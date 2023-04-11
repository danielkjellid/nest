import pytest
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError as PydanticValidationError

from nest.clients.base import BaseHTTPClient


class TestClientBaseHTTPClient:
    @pytest.mark.parametrize(
        "method_name,add_payload",
        [
            ("get", False),
            ("post", True),
            ("put", True),
            ("patch", True),
            ("delete", False),
        ],
    )
    def test_requests(self, http_client, request_mock, method_name, add_payload):
        """
        Test that the full range of methods are supported and correctly implemented, as well
        as options being passed as expected.
        """

        payload = {"foo": "bar"}

        mock_method = getattr(request_mock, method_name)
        mock_method("http://127.0.0.1/foo")

        method = getattr(http_client, method_name)
        method("/foo", json=payload if add_payload else None)

        assert request_mock.call_count == 1

        call = request_mock.request_history[0]
        assert call.method == method_name.upper()

        if add_payload:
            assert call.json() == payload

    @pytest.mark.parametrize(
        "error_status_codes", [400, 401, 403, 404, 500, 502, 503, 504]
    )
    def test_request_error(self, http_client, request_mock, error_status_codes):
        """
        Test that erroneous codes correctly throws a RequestError.
        """

        request_mock.get("http://127.0.0.1/path", status_code=error_status_codes)

        with pytest.raises(BaseHTTPClient.RequestError):
            http_client.get("/path")

    def test_serialize_response(self, http_client, request_mock):
        """
        Test that serializing a response works as expected.
        """

        class TestModelChild(BaseModel):
            id: int
            child_name: str

        class TestModelParent(BaseModel):
            id: int
            parent_name: str
            child: TestModelChild

        valid_payload = {
            "id": 1,
            "parent_name": "Parent",
            "child": {"id": 2, "child_name": "Child"},
        }
        request_mock.get("http://127.0.0.1/valid", json=valid_payload)
        response = http_client.get("/valid")
        serialized_response = http_client.serialize_response(
            serializer_cls=TestModelParent, response=response
        )

        assert serialized_response == TestModelParent(
            id=1, parent_name="Parent", child=TestModelChild(id=2, child_name="Child")
        )

        invalid_json = {"foo": "bar"}
        request_mock.get("http://127.0.0.1/invalid", json=invalid_json)
        invalid_response = http_client.get("/invalid")

        with pytest.raises(PydanticValidationError):
            http_client.serialize_response(
                serializer_cls=TestModelParent, response=invalid_response
            )
