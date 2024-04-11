from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from core_apps.search.document import ArticleDocument


class ArticleElasticsearchSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = (
            "title",
            "author_first_name",
            "author_last_name",
            "slug",
            "description",
            "body",
            "created_at",
        )
