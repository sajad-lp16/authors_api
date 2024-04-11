from collections.abc import Sequence

from django.utils import timezone

from rest_framework import serializers

from core_apps.bookmarks.serializers import BookmarkSerializer
from core_apps.comments.serializers import CommentSerializer

from core_apps.articles.models import (
    Article,
    Claps
)

from core_apps.profiles.serializers import ProfileSerializer


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, Sequence):
            raise serializers.ValidationError("Expected a list of tags")

        tag_objects = []
        for tag_name in data:
            tag_name = tag_name.strip()

            if not tag_name:
                continue
            tag_objects.append(tag_name)
        return tag_objects


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    estimated_reading_time = serializers.SerializerMethodField(read_only=True)
    banner_image = serializers.CharField(source="banner_image.url", read_only=True)
    tags = TagListField()
    bookmarks = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(instance):
        instance_creation_time = instance.created_at
        return instance_creation_time.strftime("%Y_%m_%d %H:%M:%S")

    @staticmethod
    def get_updated_at(instance):
        instance_creation_time = instance.updated_at
        return instance_creation_time.strftime("%Y_%m_%d %H:%M:%S")

    @staticmethod
    def get_estimated_reading_time(instance):
        return instance.estimated_reading

    @staticmethod
    def get_bookmarks(instance):
        bookmarks = instance.bookmarks.all()
        return BookmarkSerializer(bookmarks, many=True).data

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.body = validated_data.get("body", instance.body)
        instance.banner_image = validated_data.get("banner_image", instance.banner_image)
        instance.updated_at = timezone.now()

        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])

        instance.save()
        return instance

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "estimated_reading_time",
            "author_info",
            "view_count",
            "claps_count",
            "bookmark_count",
            "bookmarks",
            "comment_count",
            "comments",
            "average_rating",
            "description",
            "body",
            "banner_image",
            "created_at",
            "updated_at",
        ]


class ClapSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Claps
        fields = (
            "id",
            "user_first_name",
            "article_title",
        )
