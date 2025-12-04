APPS = ("infra",)

THIRD_PARTY_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_object_actions",
    "django_admin_inline_paginator",
    "django.contrib.humanize",
    "admin_extra_buttons",
    "rangefilter",
    "django_admin_filters",
    "import_export",
    "core.accounts",
)

INSTALLED_APPS = APPS + THIRD_PARTY_APPS
