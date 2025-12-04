from infra.conf.environ import env

ALLOWED_HOSTS = env("ALLOWED_HOSTS", list, default=["0.0.0.0", "127.0.0.1", "localhost"])  # noqa: S104
CSRF_TRUSTED_ORIGINS: list[str] = env("CSRF_TRUSTED_ORIGINS", list, default=[])
