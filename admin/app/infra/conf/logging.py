# Logging
# https://docs.djangoproject.com/en/4.2/topics/logging/

from collections.abc import Iterable

import structlog
from structlog.typing import EventDict, WrappedLogger

SENSITIVE_FIELDS = {
    "password",
    "passwd",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "cookie",
    "set-cookie",
    "api_key",
    "key",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # We use these formatters in our `'handlers'` configuration.
    # Probably, you won't need to modify these lines.
    # Unless, you know what you are doing.
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(ensure_ascii=False),
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"],
            ),
        },
    },
    # You can easily swap `key/value` (default) output and `json` ones.
    # Use `'json_console'` if you need `json` logs.
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "json_console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    # These loggers are required by our app:
    # - django is required when using `logger.getLogger('django')`
    # - security is required by `axes`
    "loggers": {
        "django": {
            "handlers": ["json_console"],
            "propagate": True,
            "level": "INFO",
        },
        "security": {
            "handlers": ["json_console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.request.audit": {"handlers": ["json_console"], "level": "INFO", "propagate": False},
    },
}


class RedactSensitive:
    def __init__(self, keys: Iterable[str] = ()):
        self.keys = {key.lower() for key in keys}

    def __call__(self, logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
        if isinstance(event_dict, dict):
            out = {}
            for key, value in event_dict.items():
                if self._is_sensitive(key):
                    out[key] = "***"
                else:
                    out[key] = value
            return out
        return event_dict

    def _is_sensitive(self, key: str) -> bool:
        kl = key.lower()
        return kl in self.keys


if not structlog.is_configured():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            RedactSensitive(keys=SENSITIVE_FIELDS),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
