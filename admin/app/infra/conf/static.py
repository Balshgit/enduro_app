from infra.conf.environ import env

STATIC_URL = env("STATIC_URL", str, "/static/")
STATIC_ROOT = env("STATIC_ROOT", cast=str, default="static")
