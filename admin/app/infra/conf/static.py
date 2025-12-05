from infra.conf.boilerplate import CONTENT_DIR
from infra.conf.environ import env

STATIC_URL = env("STATIC_URL", str, "/static/")
STATIC_ROOT = env("STATIC_ROOT", cast=str, default=CONTENT_DIR / "static")
STATICFILES_DIRS = [
    CONTENT_DIR / "assets",
]
