from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.units.selectors import get_units
from nest.api.factory import Partial
from .router import router
from ..records import UnitRecord

UnitListOut = Partial("UnitListOut", UnitRecord, ["id", "name", "display_name"])


@router.get("/", response=APIResponse[list[UnitListOut]])
def unit_list_api(request: HttpRequest) -> APIResponse[list[UnitListOut]]:
    units = get_units()
    data = [UnitListOut(**unit.dict()) for unit in units]

    return APIResponse(status="success", data=data)
