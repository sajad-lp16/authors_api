from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core_apps.common.models import TimeStampedModel

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", _("Male"),
        FEMALE = "E", _("Female"),
        OTHER = "O", _("Other"),

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(verbose_name=_("phone number"), max_length=30, default="+250222222")
    about_me = models.TextField(verbose_name=_("about me"), default="say something about yourself")
    gender = models.CharField(verbose_name=_("gender"), choices=Gender.choices, default=Gender.OTHER, max_length=20)
    country = CountryField(verbose_name=_("country"), default="IR")
    city = models.CharField(verbose_name=_("city"), max_length=180, default="Tehran")
    profile_photo = models.ImageField(verbose_name=_("profile photo"), default="/profile_default.png")
    twitter_handle = models.CharField(verbose_name=_("twitter handle"), max_length=20, blank=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name}s Profile"

    def follow(self, profile):
        self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)

    def check_following(self, profile):
        return self.following.filter(pkid=profile.pkid).exists()
