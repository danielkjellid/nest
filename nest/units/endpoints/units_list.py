from django.http import HttpRequest
from ninja import Schema

from nest.api.responses import APIResponse
from nest.units.selectors import UnitSelector

from .router import router


class UnitListOut(Schema):
    id: int
    name: str
    display_name: str


@router.get("/", response=APIResponse[list[UnitListOut]])
def unit_list_api(request: HttpRequest) -> APIResponse[list[UnitListOut]]:
    units = UnitSelector.all_units()
    data = [UnitListOut(**unit.dict()) for unit in units]

    return APIResponse(status="success", data=data)
