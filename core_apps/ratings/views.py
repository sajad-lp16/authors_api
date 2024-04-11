from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from core_apps.ratings.exceptions import YouHaveAlreadyRated
from core_apps.ratings.models import Rating
from core_apps.articles.models import Article
from core_apps.ratings.serializers import RatingSerializer


class RatingCreateAPIView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        article_id = self.kwargs.get("article_id")
        if article_id is None:
            raise ValidationError(_("article id is required"))

        article = get_object_or_404(Article, id=article_id)

        try:
            serializer.save(user=self.request.user, article=article)
        except IntegrityError:
            raise YouHaveAlreadyRated
