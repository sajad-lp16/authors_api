from django.contrib import admin

from core_apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article", "parent", "content", "created_at"]
    list_display_links = ["pkid", "id", "user"]

