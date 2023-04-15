from ninja import Schema
from pydantic import BaseModel
from nest.frontend.elements import FrontendElements
from nest.forms.records import FormRecord, FormElementRecord, FormElementEnumRecord
from nest.forms.form import Form
from nest.forms.fields import FormField
from nest.units.enums import UnitType
from unittest.mock import ANY


class MyChildSchema(Schema):
    id: int


class MySchema(Schema):
    val_str: str = FormField(..., help_text="Some random help text")
    val_bool: bool = FormField(False, placeholder="Is bool", col_span=1)
    val_enum: UnitType = "weight"
    val_list_int: list[int]
    val_str_none: str | None = FormField(
        ..., help_text="Optional str", default_value=None
    )
    val_child: MyChildSchema


class MyModel(BaseModel):
    val: int


class TestForm:
    def test_form_create_from_schema(self):
        """
        Test that the create_from_schema method creates a form as expected.
        """

        form = Form.create_from_schema(schema=MySchema, is_multipart_form=True)

        assert form == FormRecord[MySchema].construct(
            key="MySchema",
            is_multipart_form=True,
            expects_list=False,
            required=ANY,
            elements=[
                FormElementRecord(
                    id="valStr",
                    title="Val Str",
                    type="string",
                    enum=None,
                    parent=None,
                    default_value=None,
                    element=FrontendElements.TEXT_INPUT,
                    placeholder=None,
                    help_text="Some random help text",
                    hidden_label=False,
                    section=None,
                    col_span=None,
                ),
                FormElementRecord(
                    id="valBool",
                    title="Val Bool",
                    type="boolean",
                    enum=None,
                    parent=None,
                    default_value=False,
                    element=FrontendElements.CHECKBOX,
                    placeholder="Is bool",
                    help_text=None,
                    hidden_label=False,
                    section=None,
                    col_span=1,
                ),
                FormElementRecord(
                    id="valEnum",
                    title="Val Enum",
                    type="enum",
                    enum=[
                        FormElementEnumRecord(name="Pieces", value="pieces"),
                        FormElementEnumRecord(name="Weight", value="weight"),
                        FormElementEnumRecord(name="Volume", value="volume"),
                        FormElementEnumRecord(name="Length", value="length"),
                        FormElementEnumRecord(name="Usage", value="usage"),
                    ],
                    parent=None,
                    default_value="weight",
                    element=FrontendElements.SELECT,
                    placeholder=None,
                    help_text=None,
                    hidden_label=False,
                    section=None,
                    col_span=None,
                ),
                FormElementRecord(
                    id="valListInt",
                    title="Val List Int",
                    type="array",
                    enum=None,
                    parent=None,
                    default_value=None,
                    element=FrontendElements.MULTISELECT,
                    placeholder=None,
                    help_text=None,
                    hidden_label=False,
                    section=None,
                    col_span=None,
                ),
                FormElementRecord(
                    id="valStrNone",
                    title="Val Str None",
                    type="string",
                    enum=None,
                    parent=None,
                    default_value=None,
                    element=FrontendElements.TEXT_INPUT,
                    placeholder=None,
                    help_text="Optional str",
                    hidden_label=False,
                    section=None,
                    col_span=None,
                ),
                FormElementRecord(
                    id="id",
                    title="Id",
                    type="integer",
                    enum=None,
                    parent="val_child",
                    default_value=None,
                    element=FrontendElements.NUMBER_INPUT,
                    placeholder=None,
                    help_text=None,
                    hidden_label=False,
                    section=None,
                    col_span=None,
                ),
            ],
        )
        assert set(
            [
                "valChild",
                "valStr",
                "valListInt",
                "valStrNone",
                "valBool",
                "valEnum",
            ]
        ) == set(form.required)
