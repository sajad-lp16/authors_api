from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from authors_api.settings.local import DEFAULT_FROM_EMAIL
from core_apps.profiles.exceptions import (
    CantFollowYourself,
    CantUnFollowYourself
)
from core_apps.profiles.models import Profile
from core_apps.profiles.pagination import ProfilePagination
from core_apps.profiles.renderers import (
    ProfileJSONRenderer,
    ProfilesJSONRenderer
)
from core_apps.profiles.serializers import (
    ProfileSerializer,
    FollowingSerializer,
    UpdateProfileSerializer
)


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    pagination_class = ProfilePagination
    serializer_class = ProfileSerializer
    renderer_classes = ProfilesJSONRenderer,


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    renderer_classes = ProfileJSONRenderer,

    def get_queryset(self):
        return Profile.objects.select_related("user")

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    parser_classes = MultiPartParser,
    renderer_classes = ProfileJSONRenderer,

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serialized_instance = self.get_serializer(instance, data=request.data, partial=True)
        serialized_instance.is_valid(raise_exception=True)
        serialized_instance.save()
        return Response(serialized_instance.data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user__id=request.user.id)
        followers_profiles = profile.followers.all()
        serialized_followers = FollowingSerializer(followers_profiles, many=True)

        return Response({
            "status_code": status.HTTP_200_OK,
            "followers_count": followers_profiles.count(),
            "followers": serialized_followers.data
        }, status=status.HTTP_200_OK)


class FollowingListAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(Profile, user_id=user_id)
        following_profiles = profile.following.select_related("user").all()
        users = [profile.user for profile in following_profiles]
        serialized_users = FollowingSerializer(users, many=True)
        return Response({
            "status_code": status.HTTP_200_OK,
            "following_count": len(users),
            "following_users": serialized_users.data
        }, status=status.HTTP_200_OK)


class FollowAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):

        if user_id == request.user.id:
            raise CantFollowYourself()

        my_profile: Profile = request.user.profile
        following_profile = get_object_or_404(Profile, user__id=user_id)

        if my_profile.check_following(following_profile):
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"you are already following {following_profile.user.get_full_name}"
            }, status=status.HTTP_400_BAD_REQUEST)

        my_profile.follow(following_profile)
        send_mail(
            subject="A new user follows you",
            message=f"Hello, {following_profile.user.get_full_name}, now {my_profile.user.get_full_name} follows you!",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[following_profile.user.email],
            fail_silently=True,
        )

        return Response({
            "status_code": status.HTTP_200_OK,
            "message": f"you are now following {following_profile.user.get_full_name}"
        })


class UnFollowAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):

        if user_id == request.user.id:
            raise CantUnFollowYourself()

        following_profile = get_object_or_404(Profile, user__id=user_id)
        my_profile: Profile = request.user.profile

        if not my_profile.check_following(following_profile):
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"currently you are not following {following_profile.user.get_full_name}"
            })

        my_profile.unfollow(following_profile)
        return Response({
            "message": f"you unfollowed {following_profile.user.get_full_name}",
            "status_code": status.HTTP_200_OK
        })
