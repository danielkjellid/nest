from .base import BaseHTTPClient
from django.conf import settings
from nest.records import OdaProductDetailRecord
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from nest.exceptions import ApplicationError
import structlog

logger = structlog.getLogger()


class OdaClient(BaseHTTPClient):
    name = "oda"
    enabled = settings.ODA_SERVICE_ENABLED
    base_url = settings.ODA_SERVICE_BASE_URL
    auth_token_prefix = None
    auth_token = settings.ODA_SERVICE_AUTH_TOKEN
    request_timeout = (5, 5)

    headers = {"X-Client-Token": auth_token}

    @classmethod
    def get(cls, url: str):
        return super().get(url, headers=cls.headers)

    @classmethod
    def get_product(cls, product_id: int) -> OdaProductDetailRecord:
        try:
            response = cls.get(f"/products/{product_id}/")
            product_record = cls.serialize_response(
                serializer_cls=OdaProductDetailRecord, response=response
            )
            return product_record
        except PydanticValidationError as pexc:
            logger.error(
                "Failed to serialize product with OdaProductDetailRecord",
                serializer=OdaProductDetailRecord,
                status_code=response.status_code,
            )
            raise ApplicationError(
                message="Failed to serialize product with OdaProductDetailRecord",
                extra=pexc.errors(),
            ) from pexc
        except cls.RequestError as rexc:
            logger.error(
                "Request to product endpoint failed",
                status_code=rexc.status_code,
            )
            raise ApplicationError(
                message="Request to product endpoint failed",
                status_code=rexc.status_code,
            )
