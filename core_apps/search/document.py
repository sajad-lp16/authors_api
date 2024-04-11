from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from core_apps.articles.models import Article


@registry.register_document
class ArticleDocument(Document):
    title = fields.TextField("title")
    description = fields.TextField("description")
    body = fields.TextField("body")
    author_first_name = fields.TextField()
    author_last_name = fields.TextField()
    tags = fields.KeywordField()

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = ["created_at"]

    @staticmethod
    def prepare_author_first_name(instance):
        return instance.author.first_name

    @staticmethod
    def prepare_author_last_name(instance):
        return instance.author.last_name

    @staticmethod
    def prepare_tags(instance):
        return [tag.name for tag in instance.tags.all()]
