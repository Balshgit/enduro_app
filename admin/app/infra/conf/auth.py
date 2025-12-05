ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "accounts:log_in"
USE_REMEMBER_ME = False

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SIGN_UP_FIELDS = [
    "username",
    "first_name",
    "last_name",
    "email",
    "password1",
    "password2",
]
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ["first_name", "last_name", "email", "password1", "password2"]

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = True
