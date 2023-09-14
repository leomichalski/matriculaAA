from .base import *  # noqa
from .base import env

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# GENERAL
# ------------------------------------------------------------------------------

SECRET_KEY = 'django-insecure-59szko7c$nmh1qzwxqci&e68c9@7+a-rs=61s9d9kb=&0$2_6m'
DEBUG = env.bool("DJANGO_DEBUG", True)

#ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "54.232.197.148"]
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]



# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

