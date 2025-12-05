APPS = (
    "infra",
    "core.main",
    "core.accounts",
)

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
    # Vendor apps
    "admin_extra_buttons",
    "bootstrap4",
    "django_admin_filters",
    "import_export",
    "rangefilter",
)

INSTALLED_APPS = APPS + THIRD_PARTY_APPS
