from django.urls import path

from core_apps.profiles.views import (
    ProfileListAPIView,
    ProfileDetailAPIView,
    FollowAPIView,
    UnFollowAPIView,
    FollowerListView,
    FollowingListAPIView,
    UpdateProfileAPIView
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all_profiles"),
    path("me/", ProfileDetailAPIView.as_view(), name="my_profile"),
    path("me/update/", UpdateProfileAPIView.as_view(), name="update_my_profile"),
    path("me/followers/", FollowerListView.as_view(), name="my_followers"),
    # path("me/followings/", FollowingListAPIView.as_view(), name="my_followings"),
    path("<uuid:user_id>/follow/", FollowAPIView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnFollowAPIView.as_view(), name="unfollow")
]
