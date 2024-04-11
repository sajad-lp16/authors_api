from django.urls import path

from core_apps.bookmarks.views import (
    BookmarkCreateView,
    BookmarkDestroy
)

urlpatterns = [
    path("bookmark-article/<uuid:article_id>/", BookmarkCreateView.as_view(), name="bookmark_article"),
    path("remove-bookmark/<uuid:article_id>/", BookmarkDestroy.as_view(), name="remove_bookmark")
]
