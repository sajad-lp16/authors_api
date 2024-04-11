from rest_framework import serializers

from core_apps.ratings.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    article_title = serializers.ReadOnlyField(source="article.title")
    user_first_name = serializers.ReadOnlyField(source="user.first_name")

    class Meta:
        model = Rating
        fields = (
            "id",
            "article_title",
            "user_first_name",
            "rating",
            "review",
        )
