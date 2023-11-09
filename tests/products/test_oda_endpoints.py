from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from store_kit.http import status

from nest.products.oda.clients import OdaClient
from nest.products.oda.endpoints import (
    product_oda_import_api,
    product_oda_import_confirm_api,
)
from nest.products.oda.tests.utils import get_oda_product_response_dict

from ..factories.endpoints import (
    Endpoint,
    EndpointFactory,
    FactoryMock,
    FactoryObjMock,
    Request,
)
from ..factories.records import OdaProductDetailRecordFactory
from ..helpers.clients import authenticated_client, authenticated_staff_client

product_oda_import_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_oda_import_api"),
        method="POST",
        view_func=product_oda_import_api,
        mocks=[
            FactoryObjMock(
                OdaClient,
                "get_product",
                OdaProductDetailRecordFactory.build(
                    # Recursion bug prevents us from using build directly.
                    **get_oda_product_response_dict(id=459)
                ),
            )
        ],
        payload={"odaProductId": 459},
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to preview oda products",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"get_product": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able preview oda products",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_product": 1},
        ),
    },
)

product_oda_import_confirm_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_oda_import_confirm_api"),
        method="POST",
        view_func=product_oda_import_confirm_api,
        mocks=[FactoryMock("import_product_from_oda", None)],
        payload={"odaProductId": 459},
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to import oda products",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"import_product_from_oda": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able import oda products",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"import_product_from_oda": 1},
        ),
    },
)

request_factories = [
    product_oda_import_api_factory,
    product_oda_import_confirm_api_factory,
]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_products_oda_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
