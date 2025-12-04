import logging

import structlog
from django.http import HttpRequest
from infra.conf.installed_apps import INSTALLED_APPS
from infra.conf.middleware import MIDDLEWARE
from infra.settings import DEBUG

INSTALLED_APPS += (
    # Better debug:
    "debug_toolbar",
    "nplusone.ext.django",
)

MIDDLEWARE = (  # noqa: WPS440
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "nplusone.ext.django.NPlusOneMiddleware",
    "querycount.middleware.QueryCountMiddleware",
) + MIDDLEWARE

# Logging N+1 requests:
NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = structlog.getLogger("django")
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {
        "model": "admin.*",
    },
]


def _custom_show_toolbar(request: HttpRequest) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "infra.conf.development._custom_show_toolbar",
}
