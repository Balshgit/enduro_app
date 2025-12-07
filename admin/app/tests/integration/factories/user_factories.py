import string
from typing import Any

import factory.fuzzy
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    email = factory.Faker("email")
    username = factory.Faker("first_name", locale="en_US")
    password = factory.Faker("password")
    is_active = True

    class Meta:
        model = User
        database = "default"
        django_get_or_create = ("username",)

    @factory.post_generation
    def groups(obj, create: bool, extracted: Any, **kwargs: Any) -> None:
        if extracted:
            for group in extracted:
                obj.groups.add(group)

    @factory.post_generation
    def permissions(obj, create: bool, extracted: Any, **kwargs: Any) -> None:
        if extracted:
            for permission in extracted:
                obj.user_permissions.add(permission)


class StaffUserFactory(UserFactory):
    is_staff = True


class SuperUserFactory(StaffUserFactory):
    is_superuser = True


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group
        django_get_or_create = ("name",)

    name = factory.Faker("word")

    @factory.post_generation
    def permissions(obj, create: bool, extracted: Any, **kwargs: Any) -> None:
        if extracted:
            for permission in extracted:
                obj.permissions.add(permission)


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
        database = "default"
        django_get_or_create = ("codename",)

    name = factory.Faker("text", max_nb_chars=15)
    codename = factory.fuzzy.FuzzyText(length=10, chars=string.ascii_lowercase)

    @factory.post_generation
    def content_type(obj, create: bool, extracted: Any, **kwargs: Any) -> None:
        if extracted:
            obj.content_type = extracted

    @factory.post_generation
    def model(obj, create: bool, extracted: Any, **kwargs: Any) -> None:
        if extracted:
            obj.content_type = ContentType.objects.get_for_model(extracted)


class PermissionFactoryProxy(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
        database = "default"
        django_get_or_create = ("codename",)

    name = factory.Faker("text", max_nb_chars=15)
    codename = factory.fuzzy.FuzzyText(length=10, chars=string.ascii_lowercase)
