import logging
import os
from starlette.config import Config
from starlette.datastructures import Secret
from datetime import timedelta

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
NEST_JWT_ISSUER: str = config("NEST_JWT_ISSUER", default="nest")
NEST_JWT_SECRET_KEY: str | None = config("NEST_JWT_SECRET_KEY", default=None)
NEST_JWT_ALG: str = config("NEST_JWT_ALG", default="HS256")
NEST_JWT_ACCESS_EXP = config("NEST_JWT_ACCESS_EXP", default=timedelta(days=1))
NEST_JWT_REFRESH_EXP = config("NEST_JWT_REFRESH_EXP", default=timedelta(days=30))

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
ALEMBIC_INI_PATH: str = f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini"
ALEMBIC_REVISIONS_PATH: str = (
    f"{os.path.dirname(os.path.realpath(__file__))}/models/revisions"
)
