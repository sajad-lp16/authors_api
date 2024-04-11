from rest_framework import permissions

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from core_apps.search.document import ArticleDocument
from core_apps.search.serializers import ArticleElasticsearchSerializer


class ArticleElasticsearchAPIView(DocumentViewSet):
    document = ArticleDocument
    serializer_class = ArticleElasticsearchSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend
    ]

    filter_fields = {
        "slug": "slug.raw",
        "tags": "tags",
        "created_at": "created_at",
    }

    search_fields = (
        "title",
        "description",
        "body",
        "author_first_name",
        "author_last_name",
        "tags",
    )

    ordering_fields = {"created_at": "created_at"}
    ordering = ("-created_at",)
