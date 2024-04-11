import logging

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.files.storage import default_storage

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser
)
from rest_framework import (
    status,
    generics,
    permissions,
    filters
)

from django_filters.rest_framework import DjangoFilterBackend

from core_apps.articles.filters import ArticleFilter
from core_apps.articles.serializers import (
    ArticleSerializer,
    ClapSerializer
)
from core_apps.articles.pagination import ArticlePagination
from core_apps.common.permissions import IsOwnerOrReadonly
from core_apps.articles.renderers import (
    ArticleJSONRenderer,
    ArticlesJSONRenderer
)
from core_apps.articles.models import (
    Article,
    ArticleView,
    Claps
)

User = get_user_model()
logger = logging.getLogger(__name__)


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadonly]
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ArticleFilter
    ordering_fields = "created_at", "updated_at"
    renderer_classes = ArticlesJSONRenderer,
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"{serializer.data.get('title')} was created by {self.request.user.get_full_name}")


class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadonly]
    lookup_field = "id"
    renderer_classes = ArticleJSONRenderer,
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        if "banner_image" in self.request.FILES:
            if instance.banner_image and (instance.banner_image.name != "/profile_default.jpg"):
                default_storage.delete(instance.banner_image.path)
            instance.banner_image = self.request.FILES["banner_image"]
            instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            raise Http404

        serialized_data = self.get_serializer(instance)
        viewer_ip = self.request.META.get("REMOTE_ADDR")
        ArticleView.record_view(instance, self.request.user, viewer_ip)

        return Response(serialized_data.data)


class ClapArticleAPIView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Claps.objects.all()
    serializer_class = ClapSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadonly]

    def create(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs.get("article_id"))

        try:
            instance = Claps.objects.create(article=article, user=request.user)
        except IntegrityError:
            raise ValidationError({"detail": "you have already clapped for this article"})

        serializer = self.get_serializer(instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Claps, article__id=self.kwargs.get("article_id")).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
