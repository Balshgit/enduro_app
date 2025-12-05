import contextlib
from typing import Any

from django.template.response import TemplateResponse
from django.urls import reverse
from django_webtest import (
    DjangoTestApp as WebTestDjangoTestApp,
    WebTestMixin,
)


class OtpCompatibleWebTestMixin(WebTestMixin):
    """
    Fix possible webtest overrding django-otp results,
    because is should run directly after user is patched
    """

    def _setup_auth_middleware(self) -> None:
        webtest_auth_middleware = "django_webtest.middleware.WebtestUserMiddleware"
        self.settings_middleware.append(webtest_auth_middleware)


class WebTestApp(WebTestDjangoTestApp):
    def _update_environ(self, environ: dict[str, Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Remove HTTP_HOST header when it defaults to "testserver",
        so it does not break black tie related tests.
        """
        environ = super()._update_environ(environ, *args, **kwargs)
        if environ.get("HTTP_HOST") == "testserver":
            environ.pop("HTTP_HOST")
        return environ


def text_in_rendered_content(text: str, response: Any) -> bool:
    assert text in response.rendered_content
    return True


def get_admin_view_url(obj: Any, action: str = "add", is_list_action: bool = False) -> str:
    if (
        action
        in (
            "add",
            "changelist",
        )
        or is_list_action
    ):
        return reverse(
            f"admin:{obj._meta.app_label}_{type(obj).__name__.lower()}_{action}",
        )
    return reverse(
        f"admin:{obj._meta.app_label}_{type(obj).__name__.lower()}_{action}",
        args=(obj.pk,),
    )


def assert_admin_response_successed(response: TemplateResponse) -> None:
    assert response.status_code == 200
    with contextlib.suppress(KeyError):
        assert not response.context["errors"]
        assert not response.context["form"].errors
