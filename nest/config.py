import logging

from starlette.config import Config
from starlette.datastructures import Secret

log = logging.getLogger(__name__)

config = Config("../.env")

ENVIRONMENT = config("ENVIRONMENT", default="local")

###########
# Logging #
###########

LOG_LEVEL: str = config("LOG_LEVEL", default="warning")
LOG_OUTPUT_JSON: bool = config("LOG_OUTPUT_JSON", default=True)
LOG_SQLALCHEMY: bool = config("LOG_SQLALCHEMY", default=False)

##################
# Authentication #
##################

NEST_ENCRYPTION_KEY = config("NEST_ENCRYPTION_KEY", cast=Secret, default="supersecret")
NEST_JWT_AUDIENCE: str | None = config("NEST_JWT_AUDIENCE", default=None)
NEST_JWT_SECRET_KEY: str | None = config("NEST_JWT_SECRET_KEY", default=None)
NEST_JWT_ALG: str = config("NEST_JWT_ALG", default="HS256")
NEST_JWT_EXP: int = config("NEST_JWT_EXP", cast=int, default=14 * 24 * 60 * 60)

##########
# Sentry #
##########

SENTRY_ENABLED: bool = config("SENTRY_ENABLED", default=False)
SENTRY_DSN: str = config("SENTRY_DSN", default="")

############
# Database #
############

DATABASE_URL: str = config(
    "DATABASE_URL", default="postgresql+asyncpg://nest:nest@localhost:5433/nest"
)
