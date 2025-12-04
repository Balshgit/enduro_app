import os.path

from infra.conf.environ import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = "infra.urls"

WSGI_APPLICATION = "wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

ADMIN_URL = env("ADMIN_URL", str, "admin/")
TIME_ZONE = "Europe/Moscow"
AUTH_USER_MODEL = "accounts.CustomUser"
