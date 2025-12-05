from infra.conf.environ import env

SENTRY_DSN = env("SENTRY_DSN", cast=str, default=None)
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT", cast=str, default=None)

if not env("DEBUG") and SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
    )
