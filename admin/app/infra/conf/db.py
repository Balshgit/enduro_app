from infra.conf.environ import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB", str, "enduro"),
        "HOST": env("POSTGRES_HOST", str, "localhost"),
        "PORT": env("POSTGRES_PORT", int, 5432),
        "USER": env("POSTGRES_USER", str, "user"),
        "PASSWORD": env("POSTGRES_PASSWORD", str, "postgrespwd"),
        "CONN_MAX_AGE": env("POSTGRES_CONN_MAX_AGE", int, default=3600),
        "TEST": {
            "NAME": "enduro_test",
        },
    },
}
