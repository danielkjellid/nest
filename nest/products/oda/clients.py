from tempfile import NamedTemporaryFile
from typing import ClassVar
from urllib.request import urlopen

import structlog
from django.conf import settings
from django.core.files import File
from pydantic.error_wrappers import ValidationError as PydanticValidationError

from nest.core.clients import BaseHTTPClient
from nest.core.exceptions import ApplicationError

from .records import OdaProductDetailRecord

logger = structlog.getLogger()


class OdaClient(BaseHTTPClient):
    name = "oda"
    enabled = settings.ODA_SERVICE_ENABLED
    base_url = settings.ODA_SERVICE_BASE_URL
    auth_token_prefix = None
    auth_token = settings.ODA_SERVICE_AUTH_TOKEN
    request_timeout = (5, 5)

    headers: ClassVar = {"X-Client-Token": auth_token}

    @classmethod
    def get_product(cls, product_id: int | str) -> OdaProductDetailRecord:
        """
        Get an Oda product from their API.
        """
        product_id = int(product_id)

        try:
            logger.info("Getting product from Oda", id=product_id)
            response = cls.get(f"/products/{product_id}/", headers=cls.headers)
            product_record = cls.serialize_response(
                serializer_cls=OdaProductDetailRecord, response=response
            )
            return product_record
        except PydanticValidationError as pexc:
            logger.error(
                "Failed to serialize product with OdaProductDetailRecord",
                serializer=OdaProductDetailRecord,
                status_code=response.status_code if response else None,
                error=pexc.errors(),
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
            ) from rexc

    @classmethod
    def get_image(cls, *, url: str, filename: str) -> File | None:  # type: ignore
        """
        Copy an image from an url and save it as a File object, which allows us to save
        it directly in our model(s) as well.
        """
        logger.info("Getting product image from Oda", url=url)

        img_temp = NamedTemporaryFile(delete=True)
        with urlopen(url) as uo:
            if uo.status != 200:
                return None

            img_temp.write(uo.read())
            img_temp.flush()

        return File(img_temp, filename)
