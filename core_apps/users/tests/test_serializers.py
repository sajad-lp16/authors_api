import pytest
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from core_apps.users.serializers import (
    UserSerializer,
    CustomRegisterSerializer
)

User = get_user_model()

pytestmark = pytest.mark.django_db


def test__user_serializer(normal_user):
    serialized_data = UserSerializer(normal_user).data

    assert "id" in serialized_data
    assert "email" in serialized_data
    assert "first_name" in serialized_data
    assert "last_name" in serialized_data
    assert "gender" in serialized_data
    assert "phone_number" in serialized_data
    assert "profile_photo" in serialized_data
    assert "country" in serialized_data
    assert "city" in serialized_data


def test_to_representation_normal_user(normal_user):
    serialized_data = UserSerializer(normal_user).data

    assert serialized_data.get("admin") is None


def test_to_representation_super_user(super_user):
    serialized_data = UserSerializer(super_user).data

    assert serialized_data.get("admin") is True


def test_custom_register_serializer(mock_request):
    valid_data = {
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "testtest",
        "password1": "test_123456",
        "password2": "test_123456"
    }

    serializer = CustomRegisterSerializer(data=valid_data)
    assert serializer.is_valid()

    user = serializer.save(mock_request)

    assert user.first_name == "test"
    assert user.last_name == "testtest"
    assert user.email == "test@test.com"
    assert user.check_password("test_123456")

    invalid_data = {
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "testtest",
        "password1": "test_123456",
        "password2": "invalid"
    }

    serializer2 = CustomRegisterSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        assert serializer2.is_valid(raise_exception=True)
