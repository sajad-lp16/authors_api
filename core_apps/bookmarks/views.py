from uuid import uuid4

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from core_apps.articles.models import Article

from core_apps.bookmarks.models import Bookmark
from core_apps.bookmarks.serializers import BookmarkSerializer


class BookmarkCreateView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        if (article_id := self.kwargs.get("article_id")) is None:
            raise ValidationError("article id is required")
        article = get_object_or_404(Article, id=article_id)

        try:
            serializer.save(user=self.request.user, article=article)
        except IntegrityError:
            raise ValidationError({"detail": "you already bookmarked this article"})


class BookmarkDestroy(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        if (article_id := self.kwargs.get("article_id")) is None:
            raise ValidationError("article id is required")
        return get_object_or_404(Bookmark, article__id=article_id, user=self.request.user)
