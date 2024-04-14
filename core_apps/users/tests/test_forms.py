import pytest

from core_apps.users.user_forms import UserCreationForm
from core_apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test__user_creation_form_valid_date():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "John.doe@gmail.com",
        "password1": "Secure_password123",
        "password2": "Secure_password123",
    }

    form = UserCreationForm(data=data)

    assert form.is_valid()


def test__user_creation_form_invalid_data():
    user = UserFactory()

    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": user.email,
        "password1": "Secure_password123",
        "password2": "Secure_password123",
    }

    form = UserCreationForm(data=data)

    assert not form.is_valid()
    assert "email" in form.errors
