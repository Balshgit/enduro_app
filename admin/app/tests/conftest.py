import random
from collections.abc import Generator
from importlib import import_module
from typing import Any

import pytest
import structlog
from _pytest.fixtures import FixtureFunctionMarker
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.test.client import Client
from infra.conf.logging import SENSITIVE_FIELDS, RedactSensitive
from structlog.testing import LogCapture
from tests.integration.factories.user_factories import StaffUserFactory, SuperUserFactory
from tests.integration.utils import OtpCompatibleWebTestMixin, WebTestApp


@pytest.fixture(scope="session", autouse=True)
def faker_seed() -> int:
    return random.randint(0, 10**7)  # noqa: UP006, S311


@pytest.fixture(scope="session", autouse=True)
def _patch_on_commit_hook() -> Generator[None]:

    old_on_commit = transaction.on_commit
    transaction.on_commit = lambda func, *args, **kwargs: func()
    yield
    transaction.on_commit = old_on_commit


@pytest.fixture
def web_client(db: FixtureFunctionMarker) -> Client:
    return Client()


@pytest.fixture
def superuser(db: FixtureFunctionMarker) -> SuperUserFactory:
    return SuperUserFactory(email="admin@litres.ru", password="Xb6xL46ht")


@pytest.fixture
def staff_user(db: FixtureFunctionMarker) -> SuperUserFactory:
    return StaffUserFactory(password="Xb6xL46ht")


@pytest.fixture
def staff_client(db: FixtureFunctionMarker, staff_user: User) -> Client:
    """
    A Django test client logged in as an admin user
    """

    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def admin_client(db: FixtureFunctionMarker, superuser: User) -> Client:
    """
    A Django test client logged in as an admin user
    """

    client = Client()
    client.force_login(superuser)
    return client


@pytest.fixture
def webtest_client() -> Generator[WebTestApp]:
    """
    Yield a webtest app that is compatible with pytest func tests
    """
    attrs = {
        "csrf_checks": False,
        "app_class": WebTestApp,
    }
    webtest = type("WebTest", (OtpCompatibleWebTestMixin, object), attrs)()
    webtest._patch_settings()
    webtest.renew_app()
    yield webtest.app
    webtest._unpatch_settings()


@pytest.fixture
def session_engine() -> Any:

    return import_module(settings.SESSION_ENGINE)


@pytest.fixture
def session_store(session_engine: Any) -> Any:
    return session_engine.SessionStore()


@pytest.fixture(name="log_output")
def fixture_log_output() -> LogCapture:
    return LogCapture()


@pytest.fixture(autouse=True)
def _fixture_configure_structlog(log_output: LogCapture) -> Generator[LogCapture]:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            RedactSensitive(keys=SENSITIVE_FIELDS),
            log_output,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=False,
    )
    try:
        yield log_output
    finally:
        structlog.reset_defaults()
