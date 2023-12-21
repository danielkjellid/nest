from django.http import HttpRequest
from ninja import Router

from nest.api.responses import APIResponse

from .records import UnitRecord
from .selectors import get_units

router = Router(tags=["Router"])


@router.get("/", response=APIResponse[list[UnitRecord]])
def unit_list_api(request: HttpRequest) -> APIResponse[list[UnitRecord]]:
    units = get_units()
    return APIResponse(status="success", data=units)
