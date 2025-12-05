from core.main.views import ChangeLanguageView, IndexPageView
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from infra.conf.boilerplate import ADMIN_URL

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("", IndexPageView.as_view(), name="index"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("language/", ChangeLanguageView.as_view(), name="change_language"),
    path("accounts/", include("core.accounts.urls", namespace="accounts")),
]

urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = (
        [
            # URLs specific only to django-debug-toolbar:
            path("__debug__/", include(debug_toolbar.urls)),  # noqa: DJ05
        ]
        + urlpatterns
        + static(
            # Serving media files in development only:
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    )
