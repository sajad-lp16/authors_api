import pytest

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core_apps.users.views import CustomUserDetailsView

pytestmark = pytest.mark.django_db


def test__authentication_requirement(normal_user):
    client = APIClient()
    api_url = reverse("user_details")

    response = client.get(api_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(normal_user)

    response = client.get(api_url)
    assert response.status_code == status.HTTP_200_OK


def test__retrieve_user_details(normal_user):
    client = APIClient()
    api_url = reverse("user_details")
    client.force_authenticate(normal_user)

    response = client.get(api_url)

    assert response.data["first_name"] == normal_user.first_name
    assert response.data["last_name"] == normal_user.last_name
    assert response.data["email"] == normal_user.email


def test__update_user_details(normal_user):
    client = APIClient()
    api_url = reverse("user_details")
    client.force_authenticate(normal_user)

    new_first_name = "UpdatedFirstName"
    new_last_name = "UpdatedLastName"

    updated_data = {
        "first_name": new_first_name,
        "last_name": new_last_name
    }

    response = client.patch(api_url, data=updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == new_first_name
    assert response.data["last_name"] == new_last_name

    assert normal_user.first_name == new_first_name
    assert normal_user.last_name == new_last_name


def test__get_queryset_empty(normal_user):
    client = APIClient()
    api_url = reverse("user_details")
    client.force_authenticate(normal_user)

    response = client.get(api_url)

    view = CustomUserDetailsView()
    view.request = response.wsgi_request
    queryset = view.get_queryset()

    assert queryset.count() == 0
