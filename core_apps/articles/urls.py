from django.urls import path

from core_apps.articles.views import (
    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path("", ArticleListCreateAPIView.as_view(), name="article_list_create"),
    path("<uuid:id>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="article_retrieve_destroy"),
]
