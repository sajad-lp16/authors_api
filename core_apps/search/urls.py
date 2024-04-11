from django.urls import path

from core_apps.search.views import ArticleElasticsearchAPIView

urlpatterns = [
    path("search/", ArticleElasticsearchAPIView.as_view({"get": "list"}), name="search"),
]
