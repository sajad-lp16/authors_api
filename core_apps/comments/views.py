from uuid import UUID

from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from core_apps.common.permissions import IsOwnerOrReadonly

from core_apps.articles.models import Article

from core_apps.comments.models import Comment
from core_apps.comments.serializers import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        return article.comments.filter(parent__isnull=True)

    def create(self, request, *args, **kwargs):
        article_id = self.kwargs.get("article_id")
        request_body_data = dict(request.data)
        parent_uuid_str = request_body_data.pop("parent", None)

        serializer = self.get_serializer(data=request_body_data)

        parent = None

        if parent_uuid_str is not None:
            try:
                parent_uuid = UUID(parent_uuid_str)
                parent = Comment.objects.get(id=parent_uuid)
            except Comment.DoesNotExist:
                raise NotFound({"detail": "parent comment if not found"})
            except ValueError:
                raise ValidationError({"detail": "invalid parent id"})

        article = get_object_or_404(Article, id=article_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, user=self.request.user, parent=parent)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Comment.objects.all()
    lookup_field = "id"
