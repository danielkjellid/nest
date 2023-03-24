import warnings
from pathlib import Path

import environ
import structlog

###############
# Environment #
###############

warnings.filterwarnings("ignore", message="Error reading .env", category=UserWarning)
env = environ.Env()

# If ENV_PATH is set, load that file first, so it wins over any conflicting
# environment variables in `.env`
if "ENV_PATH" in env:
    env.read_env(env.str("ENV_PATH"))

env.read_env(".env")

BASE_DIR = (Path(__file__).parent / "..").resolve()
APP_DIR = Path(__file__).parent.resolve()

DEBUG = env.bool("DEBUG", default=False)

ENVIRONMENT = env.str("ENVIRONMENT", default="local")

#################
# Django basics #
#################

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="supersecret-key")

ROOT_URLCONF = "nest.urls"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
WSGI_APPLICATION = "nest.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

################
# Localization #
################

# Local time zone for this installation.
TIME_ZONE = "Europe/Oslo"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

DATE_FORMAT = "%d. %B %Y"
DATETIME_FORMAT = "%d. %B %Y %H:%M"
DATETIME_INPUT_FORMATS = ["%d. %B %Y %H:%M"]

##############
# Middleware #
##############

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "nest.middlewares.GenericLoggingMiddleware",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.locale.LocaleMiddleware",
]

########
# Apps #
########

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = ["django_s3_storage", "django_vite", "ninja"]

PROJECT_APPS = ["nest"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

###############
# Django vite #
###############

DJANGO_VITE_DEV_MODE = env.bool("DJANGO_VITE_DEV_MODE", default=True)
DJANGO_VITE_DEV_SERVER_HOST = env.str(
    "DJANGO_VITE_DEV_SERVER_HOST", default="localhost"
)
DJANGO_VITE_DEV_SERVER_PORT = env.int("DJANGO_VITE_DEV_SERVER_PORT", default=9002)
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "static" / "vite_output"

#########
# Files #
#########

DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
AWS_REGION = env.str("AWS_REGION", default="local")
AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="nest")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="nesttestpassword")
AWS_ENDPOINT_URL = env.str("AWS_ENDPOINT_URL", default="http://localhost:9000")

# Media
MEDIA_URL = env.str("MEDIA_URL", default="/media/")
AWS_S3_ADDRESSING_STYLE = "auto"
AWS_S3_BUCKET_AUTH = False
AWS_S3_BUCKET_NAME = env.str("AWS_S3_BUCKET_NAME", default="dev")
AWS_S3_ENDPOINT_URL = AWS_ENDPOINT_URL
AWS_S3_FILE_OVERWRITE = False
AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year.
AWS_S3_SIGNATURE_VERSION = None

# Static files
STATIC_URL = env.str("STATIC_URL", default="/static/")
# Because we service vite as a static asset, we cannot use minio for static files
# locally
if DEBUG:
    STATIC_ROOT = BASE_DIR / "static"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]
else:
    STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    AWS_S3_BUCKET_AUTH_STATIC = False
    AWS_S3_BUCKET_NAME_STATIC = env.str("AWS_S3_BUCKET_NAME_STATIC", default="dev")
    AWS_S3_ENDPOINT_URL_STATIC = AWS_ENDPOINT_URL
    AWS_S3_KEY_PREFIX_STATIC = "static"

#############
# Templates #
#############

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APP_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = "nest.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

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

#############
# Databases #
#############

DATABASES = {
    "default": env.db_url(
        "DATABASE_URL", default="postgresql://nest:nest@localhost:5433/nest"
    ),
}

LOG_SQL = env.bool("LOG_SQL", default=False)

QUERY_COUNT_WARNING_THRESHOLD = 25
QUERY_DURATION_WARNING_THRESHOLD = 300  # in ms

if DEBUG:
    MIDDLEWARE = ["nest.middlewares.QueryCountWarningMiddleware", *MIDDLEWARE]

###########
# Logging #
###########

log_renderer: structlog.types.Processor = (
    structlog.dev.ConsoleRenderer(colors=True, sort_keys=True)  # type: ignore
    if DEBUG
    else structlog.processors.JSONRenderer()
)

shared_log_processors: list[structlog.types.Processor] = [
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
]

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        *shared_log_processors,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": log_renderer,
            "foreign_pre_chain": shared_log_processors,
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "console": {
            "filters": ["require_debug_true"],
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

#####################
# Django Extensions #
#####################

try:
    import django_extensions  # noqa: 401 # pylint: disable=unused-import
except ImportError:
    DJANGO_EXTENSIONS_INSTALLED = False
else:
    DJANGO_EXTENSIONS_INSTALLED = True

if DJANGO_EXTENSIONS_INSTALLED:
    INSTALLED_APPS += ["django_extensions"]
