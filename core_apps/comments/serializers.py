from rest_framework import serializers

from core_apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment

        fields = (
            "id",
            "user_first_name",
            "article_title",
            "content",
            "parent",
            "replies",
            "created_at",
        )

    @classmethod
    def get_replies(cls, instance: Comment):
        return cls(instance.replies.all(), many=True).data
