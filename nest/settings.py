import warnings
from pathlib import Path

import environ
import sentry_sdk
import structlog
from sentry_sdk.integrations.django import DjangoIntegration

from nest.frontend.components import FrontendComponents

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
IS_PRODUCTION = env.bool(
    "IS_PRODUCTION", default=(not ENVIRONMENT == "local" and not DEBUG)
)

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
    "nest.core.middlewares.GenericLoggingMiddleware",
    "hijack.middleware.HijackUserMiddleware",
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

THIRD_PARTY_APPS = ["django_s3_storage", "django_vite", "hijack", "ninja"]

PROJECT_APPS = [
    "nest.api",
    "nest.core",
    "nest.frontend",
    "nest.homes",
    "nest.products",
    "nest.units",
    "nest.users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

###############
# Django vite #
###############

DJANGO_VITE_DEV_MODE = env.bool("DJANGO_VITE_DEV_MODE", default=True)
DJANGO_VITE_DEV_SERVER_HOST = env.str(
    "DJANGO_VITE_DEV_SERVER_HOST", default="localhost"
)
DJANGO_VITE_DEV_SERVER_PORT = env.int("DJANGO_VITE_DEV_SERVER_PORT", default=9002)
DJANGO_VITE_ASSETS_PATH = BASE_DIR / "public" / "vite_output"
DJANGO_VITE_MANIFEST_PATH = DJANGO_VITE_ASSETS_PATH / "manifest.json"

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
    STATIC_ROOT = BASE_DIR / "public"
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
        "DIRS": [str(APP_DIR / "frontend" / "templates")],
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

AUTH_USER_MODEL = "users.User"

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

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "login"

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
    MIDDLEWARE += ["nest.core.middlewares.QueryCountWarningMiddleware"]

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

##########
# Hijack #
##########

HIJACK_PERMISSION_CHECK = "hijack.permissions.superusers_and_staff"
HIJACK_INSERT_BEFORE = None

##################
# OpenAPI Schema #
##################

OPENAPI_AUTO_GENERATE = env.str("OPENAPI_AUTO_GENERATE", default=DEBUG)

#######
# Oda #
#######

ODA_SERVICE_ENABLED = env.bool("ODA_SERVICE_ENABLED", default=False)
ODA_SERVICE_BASE_URL = env.str("ODA_SERVICE_BASE_URL", default="https://oda.com/api/v1")
ODA_SERVICE_AUTH_TOKEN = env.str("ODA_SERVICE_AUTH_TOKEN", default="supersecrettoken")

##########
# Sentry #
##########

SENTRY_DSN = env.str("SENTRY_DSN", default=None)

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

#########
# Forms #
#########

FORM_COMPONENT_MAPPING_DEFAULTS = {
    "string": FrontendComponents.TEXT_INPUT,
    "text": FrontendComponents.TEXT_INPUT,
    "integer": FrontendComponents.NUMBER_INPUT,
    "boolean": FrontendComponents.CHECKBOX,
    "enum": FrontendComponents.SELECT,
    "array": FrontendComponents.MULTISELECT,
    "file": FrontendComponents.FILE_INPUT,
    "image": FrontendComponents.FILE_INPUT,
    "number": FrontendComponents.NUMBER_INPUT,
    "object": FrontendComponents.NUMBER_INPUT,
}

#####################
# Django Extensions #
#####################

try:
    import django_extensions  # noqa: 401
except ImportError:
    DJANGO_EXTENSIONS_INSTALLED = False
else:
    DJANGO_EXTENSIONS_INSTALLED = True

if DJANGO_EXTENSIONS_INSTALLED:
    INSTALLED_APPS += ["django_extensions"]

##################
# Django Toolbar #
##################

DJANGO_DEBUG_TOOLBAR_ENABLED = env.bool("DEBUG_TOOLBAR_ENABLED", default=True)

try:
    import debug_toolbar  # noqa: 401
except ImportError:
    DJANGO_DEBUG_TOOLBAR_INSTALLED = False
else:
    DJANGO_DEBUG_TOOLBAR_INSTALLED = True

if DEBUG and DJANGO_DEBUG_TOOLBAR_INSTALLED and DJANGO_DEBUG_TOOLBAR_ENABLED:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = ["127.0.0.1"]
