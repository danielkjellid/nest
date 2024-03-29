from unittest.mock import MagicMock

import pytest
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from store_kit.http import status

from nest.products.core.endpoints import (
    product_create_api,
    product_detail_api,
    product_edit_api,
    product_list_api,
)

from ..factories.endpoints import (
    Endpoint,
    EndpointFactory,
    FactoryMock,
    Request,
)
from ..factories.records import ProductRecordFactory
from ..helpers.clients import authenticated_client, authenticated_staff_client

product_list_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_list_api"),
        view_func=product_list_api,
        mocks=[FactoryMock("get_products", [ProductRecordFactory.build()])],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are able to retrieve a list of products.",
            client=authenticated_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_products": 1},
        ),
    },
)

product_create_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_create_api"),
        method="POST",
        view_func=product_create_api,
        mocks=[FactoryMock("create_product", None)],
        content_type=MULTIPART_CONTENT,
        payload={
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": 1,
            "supplier": "Cool supplier",
            "is_available": True,
            "is_synced": True,
        },
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to create new products.",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"create_product": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to create new products",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_201_CREATED,
            expected_mock_calls={"create_product": 1},
        ),
    },
)

product_edit_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_edit_api", args=[1]),
        method="POST",
        view_func=product_edit_api,
        mocks=[FactoryMock("edit_product", None)],
        content_type=MULTIPART_CONTENT,
        payload={
            "name": "Some cool product",
            "gross_price": "100.00",
            "unit_quantity": "1",
            "unit": 1,
            "supplier": "Cool supplier",
            "is_available": True,
            "is_synced": True,
        },
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are unable to edit existing products",
            client=authenticated_client,
            expected_status_code=status.HTTP_401_UNAUTHORIZED,
            expected_mock_calls={"edit_product": 0},
        ),
        "staff_request": Request(
            help="Test that staff users are able to edit existing products",
            client=authenticated_staff_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"edit_product": 1},
        ),
    },
)

product_detail_api_factory = EndpointFactory(
    endpoint=Endpoint(
        url=reverse("api-1.0.0:product_detail_api", args=[1]),
        view_func=product_detail_api,
        mocks=[FactoryMock("get_product", ProductRecordFactory.build())],
    ),
    requests={
        "authenticated_request": Request(
            help="Test that normal users are able to retrieve product details",
            client=authenticated_client,
            expected_status_code=status.HTTP_200_OK,
            expected_mock_calls={"get_product": 1},
        ),
    },
)

request_factories = [
    product_create_api_factory,
    product_list_api_factory,
    product_edit_api_factory,
    product_detail_api_factory,
]


@pytest.mark.parametrize("factory", request_factories)
@pytest.mark.django_db
def test_products_core_endpoints(factory: EndpointFactory, mocker: MagicMock) -> None:
    factory.make_requests_and_assert(mocker)
