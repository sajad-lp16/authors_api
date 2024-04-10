from rest_framework import serializers

from django_countries.serializer_fields import CountryField

from core_apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.CharField(source="user.get_full_name")
    profile_photo = serializers.SerializerMethodField(read_only=True)
    country = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_photo",
            "phone_number",
            "gender",
            "country",
            "city",
            "twitter_handle",
            "about_me",
            "full_name"
        ]


class FollowingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile

        fields = [
            "first_name",
            "last_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
        ]
