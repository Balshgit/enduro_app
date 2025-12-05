from pathlib import Path

from infra.conf.environ import env

BASE_DIR = Path(__file__).resolve().parents[3]
CONTENT_DIR = BASE_DIR / "content"

ROOT_URLCONF = "infra.urls"

WSGI_APPLICATION = "wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

ADMIN_URL = env("ADMIN_URL", str, "admin/")
TIME_ZONE = "Europe/Moscow"

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

USE_I18N = True
LANGUAGE_CODE = "ru"

APPEND_SLASH = False
