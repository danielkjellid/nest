import pytest
from pydantic import BaseModel

from nest.core.utils import Exclude, Partial
from nest.forms.fields import FormField


class TestModel(BaseModel):
    name: str
    age: int
    is_active: bool
    gender: str | None = FormField(..., description="Some gener attr")


def test_core_util_pydantic_partial():
    fields = ["name", "gender"]

    PartialModel = Partial("PartialModel", TestModel, fields)
    partial_model_fields = PartialModel.__fields__
    original_model_fields = TestModel.__fields__

    assert issubclass(PartialModel, BaseModel)
    assert set(fields) == set(partial_model_fields.keys())

    for field in fields:
        original_field = original_model_fields[field]
        partial_field = partial_model_fields[field]

        assert original_field.name == partial_field.name
        assert original_field.type_ == partial_field.type_
        assert original_field.required == partial_field.required

    with pytest.raises(ValueError):
        Partial("Testing", TestModel, ["field_does_not_exist"])


def test_core_util_pydantic_exclude():
    excluded_fields = ["name", "age"]

    ExcludedModel = Exclude("ExcludedModel", TestModel, excluded_fields)
    excluded_model_fields = ExcludedModel.__fields__
    original_model_fields = TestModel.__fields__

    original_fields_name = [f.name for f in original_model_fields.values()]
    picked_fields = set(original_fields_name) - set(excluded_fields)

    assert issubclass(ExcludedModel, BaseModel)
    assert picked_fields == set(excluded_model_fields.keys())

    for field in picked_fields:
        original_field = original_model_fields[field]
        partial_field = excluded_model_fields[field]

        assert original_field.name == partial_field.name
        assert original_field.type_ == partial_field.type_
        assert original_field.required == partial_field.required

    with pytest.raises(ValueError):
        Exclude("Testing", TestModel, ["field_does_not_exist"])
