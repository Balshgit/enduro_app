import http
from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse

from tests.integration.factories.user_factories import (
    PermissionFactory,
    StaffUserFactory,
    SuperUserFactory,
    UserFactory,
)

pytestmark = [
    pytest.mark.django_db(
        databases=["default"],
        transaction=True,
    )
]


def test_staff_cant_change_another_admin_password_email(web_client: Client) -> None:
    admin = SuperUserFactory(
        email="admin@example.com", username="admin", permissions=[PermissionFactory(model=User, codename="change_user")]
    )
    staff_user = StaffUserFactory(email="user@example.com", username="test_admin", password="5htetGqZZ2")
    was_superuser = admin.is_superuser
    now = datetime.now()  # noqa: DTZ005

    web_client.force_login(staff_user)

    response = web_client.post(
        reverse("admin:auth_user_change", args=[admin.pk]),
        {
            "email": "hacked@example.com",
            "username": "hacked",
            "is_superuser": True,
            "is_staff": True,
            "date_joined_0": now.date(),
            "date_joined_1": now.time(),
        },
        user=staff_user,
    )
    assert response.status_code == http.HTTPStatus.FORBIDDEN

    admin.refresh_from_db()
    assert admin.email == "admin@example.com"
    assert admin.username == "admin"
    assert admin.is_superuser == was_superuser
    assert admin.is_staff
    assert admin.is_active


def test_admin_can_change_another_staff_or_admin_password(
    web_client: Client,
) -> None:
    super_user = SuperUserFactory(email="admin@example.com", username="superuser", password="password")
    regular_user = UserFactory(
        email="user@example.com",
        username="regular",
        password="5htetGqZZ2",
        date_joined=datetime.now(),  # noqa: DTZ005
    )
    now = datetime.now()  # noqa: DTZ005

    web_client.force_login(super_user)

    response = web_client.post(
        reverse("admin:auth_user_change", args=[regular_user.id]),
        {
            "is_staff": True,
            "is_active": True,
            "is_superuser": True,
            "email": regular_user.email,
            "username": regular_user.username,
            "date_joined_0": now.date(),
            "date_joined_1": now.time(),
        },
        user=super_user,
    )

    # 200 means the form is being re-displayed with errors
    assert response.status_code == http.HTTPStatus.FOUND

    regular_user.refresh_from_db()

    assert regular_user.email == "user@example.com"
    assert regular_user.username == "regular"
    assert regular_user.is_superuser
    assert regular_user.is_staff
    assert regular_user.is_active


def test_user_manager() -> None:
    User.objects.create_user(email="regular_user@litres.ru", password="secret", username="regular_user")
    User.objects.create_superuser(email="admin@litres.ru", password="secret", username="admin_user")

    assert User.objects.filter(email="regular_user@litres.ru").exists()
    assert User.objects.filter(email="admin@litres.ru").exists()

    regular_user = User.objects.get(email="regular_user@litres.ru")
    admin_user = User.objects.get(email="admin@litres.ru")

    assert not regular_user.is_superuser
    assert regular_user.username == "regular_user"
    assert regular_user.is_active

    assert admin_user.is_staff
    assert admin_user.is_superuser
    assert admin_user.is_active
    assert admin_user.username == "admin_user"
