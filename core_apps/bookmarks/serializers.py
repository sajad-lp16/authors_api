from rest_framework import serializers

from core_apps.bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Bookmark
        fields = (
            "article_title",
            "user_first_name"
        )
