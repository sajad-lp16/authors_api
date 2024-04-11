from django.urls import path

from core_apps.ratings.views import RatingCreateAPIView

urlpatterns = [
    path("rate-article/<uuid:article_id>/", RatingCreateAPIView.as_view(), name="article_create"),
]
