import pytest

from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


def test__create_normal_user(normal_user: User):
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None

    assert not normal_user.is_staff
    assert not normal_user.is_superuser
    assert normal_user.is_active


def test__create_superuser(super_user: User):
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.pkid is not None

    assert super_user.is_staff
    assert super_user.is_superuser
    assert super_user.is_active


def test__get_full_name(normal_user: User):
    full_name = normal_user.get_full_name

    expected_full_name = f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    assert expected_full_name == full_name


def test__get_short_name(normal_user):
    assert normal_user.get_short_name == normal_user.first_name


def test__update_user(normal_user: User):
    new_first_name = "John"
    new_last_name = "Doe"
    new_password = "JohnDoe"

    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.set_password(new_password)
    normal_user.save()

    updated_user = User.objects.get(pk=normal_user.pkid)

    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name
    assert updated_user.check_password(new_password)


def test__delete_user(normal_user: User):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_pk)


def test__user_str(normal_user: User):
    assert str(normal_user) == normal_user.first_name


def test__normal_user_email_is_normalized(normal_user: User):
    email = normal_user.email
    assert email == email.lower()


def test__superuser_email_is_normalized(super_user: User):
    email = super_user.email
    assert email == email.lower()


def test__user_email_incorrect(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="realstate.comm")
    assert str(err.value) == "you must provide a valid email address!"


def test__create_user_without_first_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "first name is required"


def test__create_user_without_last_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "last name is required"


def test__create_user_without_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "email is required!"


def test__create_user_without_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None)
    assert str(err.value) == "user must have password"


def test__superuser_email_incorrect(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="realstate.comm", is_staff=True, is_superuser=True)
    assert str(err.value) == "you must provide a valid email address!"


def test__create_superuser_without_first_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None, is_staff=True, is_superuser=True)
    assert str(err.value) == "first name is required"


def test__create_superuser_without_last_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None, is_staff=True, is_superuser=True)
    assert str(err.value) == "last name is required"


def test__create_superuser_without_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_staff=True, is_superuser=True)
    assert str(err.value) == "superuser must have email"


def test__create_superuser_without_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_staff=True, is_superuser=True)
    assert str(err.value) == "superuser must have password"


def test__create_superuser_with_false_is_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=False, is_superuser=True)
    assert str(err.value) == "superuser must have is_staff=True"
