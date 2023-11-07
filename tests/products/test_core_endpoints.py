import pytest
from ..helpers.factories import EndpointFactory, EndpointRequest, FactoryMock
from ..helpers.clients import authenticated_client, authenticated_staff_client
from django.urls import reverse
from django.test.client import MULTIPART_CONTENT
from decimal import Decimal
from nest.products.core.endpoints import (
    product_create_api,
    product_edit_api,
    product_list_api,
    product_detail_api,
)
from nest.products.core.records import ProductRecord, ProductClassifiersRecord
from nest.units.records import UnitRecord
from nest.units.enums import UnitType
from store_kit.http import status

payload = {
    "name": "Some cool product",
    "gross_price": "100.00",
    "unit_quantity": "1",
    "unit": 1,
    "supplier": "Cool supplier",
    "is_available": True,
    "is_synced": True,
}

product_create_api_factory = EndpointFactory(
    url=reverse("api-1.0.0:product_create_api"),
    method="POST",
    endpoint=product_create_api,
    mocks=[FactoryMock("create_product", None)],
    content_type=MULTIPART_CONTENT,
    payload=payload,
)

product_create_api_anonymous_request = EndpointRequest(
    endpoint_factory=product_create_api_factory,
    client=authenticated_client,
)
product_create_api_staff_request = EndpointRequest(
    endpoint_factory=product_create_api_factory,
    client=authenticated_staff_client,
)

product_edit_api_factory = EndpointFactory(
    url=reverse("api-1.0.0:product_edit_api", args=[1]),
    method="POST",
    endpoint=product_edit_api,
    mocks=[FactoryMock("edit_product", None)],
    content_type=MULTIPART_CONTENT,
    payload=payload,
)

product_edit_api_anonymous_request = EndpointRequest(
    endpoint_factory=product_edit_api_factory,
    client=authenticated_client,
)
product_edit_api_staff_request = EndpointRequest(
    endpoint_factory=product_edit_api_factory,
    client=authenticated_staff_client,
)

product_list_api_anonymous_request = EndpointRequest(
    endpoint_factory=EndpointFactory(
        url=reverse("api-1.0.0:product_list_api"),
        endpoint=product_list_api,
        mocks=[FactoryMock("get_products", [])],
    ),
    client=authenticated_client,
)

product_detail_api_anonymous_request = EndpointRequest(
    endpoint_factory=EndpointFactory(
        url=reverse("api-1.0.0:product_detail_api", args=[1]),
        endpoint=product_detail_api,
        mocks=[
            FactoryMock(
                "get_product",
                ProductRecord(
                    id=1,
                    name="Product",
                    full_name="Some product",
                    gross_price=Decimal("100.00"),
                    gross_unit_price=None,
                    unit=UnitRecord(
                        id=1,
                        name="Gram",
                        abbreviation="g",
                        unit_type=UnitType.WEIGHT,
                        base_factor=Decimal("1000"),
                        display_name="Gram (g)",
                        is_base_unit=True,
                        is_default=True,
                    ),
                    unit_quantity=Decimal("1.00"),
                    oda_id=None,
                    oda_url=None,
                    is_available=True,
                    is_synced=True,
                    last_synced_at=None,
                    thumbnail_url=None,
                    gtin=None,
                    supplier=None,
                    display_price="100.00",
                    is_oda_product=False,
                    last_data_update=None,
                    ingredients=None,
                    allergens=None,
                    classifiers=ProductClassifiersRecord(
                        contains_gluten=False, contains_lactose=False
                    ),
                    energy_kj=None,
                    energy_kcal=None,
                    fat=None,
                    fat_saturated=None,
                    fat_monounsaturated=None,
                    fat_polyunsaturated=None,
                    carbohydrates=None,
                    carbohydrates_sugars=None,
                    carbohydrates_starch=None,
                    carbohydrates_polyols=None,
                    fibres=None,
                    protein=None,
                    salt=None,
                    sodium=None,
                ),
            ),
            FactoryMock("get_log_entries_for_object", []),
            FactoryMock("get_nutrition_table", []),
        ],
    ),
    client=authenticated_client,
)

endpoints = [
    (product_create_api_anonymous_request, status.HTTP_401_UNAUTHORIZED, [0]),
    (product_create_api_staff_request, status.HTTP_200_OK, [1]),
    (product_edit_api_anonymous_request, status.HTTP_401_UNAUTHORIZED, [0]),
    (product_edit_api_staff_request, status.HTTP_200_OK, [1]),
    (product_list_api_anonymous_request, status.HTTP_200_OK, [1]),
    (product_detail_api_anonymous_request, status.HTTP_200_OK, [1, 1, 1]),
]


@pytest.mark.parametrize("endpoint_request, status_code, call_counts", endpoints)
@pytest.mark.django_db
def test_products_core_endpoints(
    endpoint_request: EndpointRequest, status_code, call_counts, mocker
) -> None:
    endpoint_request.make_request_and_assert(
        mocker, status_code=status_code, call_counts=call_counts
    )
