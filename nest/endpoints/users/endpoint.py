from ninja import Schema
from .router import router


class TestSchema(Schema):
    id: int


@router.get("test/", response={200: TestSchema})
def test_endpoint(request):
    return TestSchema(id=1)
