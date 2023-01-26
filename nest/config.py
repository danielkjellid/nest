import logging
import os

from starlette.config import Config
from starlette.datastructures import Secret

log = logging.getLogger(__name__)

config = Config("../.env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENVIRONMENT = config("ENVIRONMENT", default="local")

##################
# Authentication #
##################

NEST_ENCRYPTION_KEY = config("NEST_ENCRYPTION_KEY", cast=Secret, default="supersecret")
NEST_JWT_AUDIENCE = config("NEST_JWT_AUDIENCE", default=None)
NEST_JWT_SECRET_KEY = config("NEST_JWT_SECRET_KEY", default=None)
NEST_JWT_ALG = config("NEST_JWT_ALG", default="HS256")
NEST_JWT_EXP = config("NEST_JWT_EXP", cast=int, default=14 * 24 * 60 * 60)

##########
# Sentry #
##########

SENTRY_ENABLED = config("SENTRY_ENABLED", default="")
SENTRY_DSN = config("SENTRY_DSN", default="")

############
# Database #
############

DATABASE_URL = config("DATABASE_URL", default="nest:nest@localhost:5438/nest")

###########
# Alembic #
###########

ALEMBIC_REVISION_PATH = config(
    "ALEMBIC_REVISION_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/database/revisions/",
)
ALEMBIC_INI_PATH = config(
    "ALEMBIC_INI_PATH",
    default=f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini",
)
