from django.urls import path

from core_apps.comments.views import (
    CommentListCreateAPIView,
    CommentUpdateDeleteAPIView
)

urlpatterns = [
    path("article/<uuid:article_id>/", CommentListCreateAPIView.as_view(), name="comment_list_create"),
    path("<uuid:id>/", CommentUpdateDeleteAPIView.as_view(), name="comment_update_delete"),
]
