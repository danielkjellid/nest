from ninja import Schema
from .router import router
from time import sleep


class TestSchema(Schema):
    id: int


@router.get("test/", response={200: TestSchema})
def test_endpoint(request):
    sleep(2)
    return TestSchema(id=1)
