import django_stubs_ext
from infra.conf.environ import env
from split_settings.tools import include

STAGE = env("STAGE")
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)

django_stubs_ext.monkeypatch()

DATETIME_FORMAT = "Y-m-d H:i:s"

_base_settings = (
    "conf/boilerplate.py",
    "conf/db.py",
    "conf/http.py",
    "conf/i18n.py",
    "conf/installed_apps.py",
    "conf/logging.py",
    "conf/middleware.py",
    "conf/sentry.py",
    "conf/static.py",
    "conf/storage.py",
    "conf/templates.py",
)

if DEBUG and env("STAGE", str, "dev") == "dev":
    _base_settings += ("conf/development.py",)  # type: ignore

include(*_base_settings)
