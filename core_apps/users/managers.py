from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(_("you must provide a valid email address!"))

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not first_name:
            raise ValueError(_("first name is required"))

        if not last_name:
            raise ValueError(_("last name is required"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("email is required!"))

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save(using=self._db)
        return True

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("superuser must have is_staff=True"))

        if not extra_fields.get("is_superuser"):
            raise ValueError(_("superuser must have is_superuser=True"))

        if not extra_fields.get("is_active"):
            raise ValueError(_("superuser must have is_active=True"))

        if not password:
            raise ValueError(_("superuser must have password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("superuser must have email"))

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return True
