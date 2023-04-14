from pydantic import BaseModel, StrictBool, StrictInt, StrictStr
from nest.frontend.elements import FrontendElements
from pydantic.generics import GenericModel
from typing import TypeVar, Generic

T = TypeVar("T")


class FormElementEnumRecord(BaseModel):
    """
    A form block enum provides enum values to be used in a select.

    * name:
        The display name of the enum property.

    * value:
        The value to use.
    """

    name: str
    value: int | bool | str


class FormElementRecord(BaseModel):
    """
    A form element is a html element used to build a form. Can for example be a
    checkbox, input, etc.

    * id:
        The id to use for the form block. Used to set the id on the element itself, but
        also in the FormSectionRecord to group elements in sections.

    * title:
        Title of element. What the element is visually identified by.

    * type:
        Type of element value. Set by generated definition spec.

    * enum:
        Enumeration values in the form of FormElementEnumRecord available to use.

    * parent:
        As we support nested schemas, the spec generated creates reference values which
        we need later when we're going to post the form. Will effectively result in a
        key-value property where the key is the parent id and value is the schema as an
        object.

    * default_value:
        The default value to use to prefill/preselect a value in the element.

    * element:
        The frontend element to render of type FrontendFormElements.

    * placeholder:
        Placeholder value to pre-populate form element with.

    * help_text:
        A str which can help guide the user or explain more about the value of the
        element. Will appear as a text bellow the element.

    * hidden_label:
        Set the label on top of the form element to only appear on screen readers.

    * section:
        A section groups different elements of the form and adds them together in a
        section.

    * col_span:
        Column span of the element. Only valid if the element is part of a section with
        defined amount of columns.
    """

    id: str
    title: str | None
    type: str | None
    enum: list[FormElementEnumRecord] | None
    parent: str | None
    default: StrictInt | StrictStr | StrictBool | None
    element: FrontendElements | None
    placeholder: str | None
    help_text: str | None
    hidden_label: bool | None = False
    section: str | None = None
    col_span: int | None = None


class FormRecord(GenericModel, Generic[T]):
    """
    A form record represents a complete form.

    * key:
        Effectively the "id" of the form.

    * is_multipart_form:
        Convert the form to multipart before posting it to an endpoint.

    * expects_list:
        Should be True if the endpoint in question expects a list of records instead of
        a single record as payload. E.g. for bulk creation and so on.

    * required:
        A list of form element ids that are required.

    * sections:
        A list of form sections of type FormSectionRecord.

    * elements:
        A list of all elements to render in the form.
    """

    key: str
    is_multipart_form: bool = False
    expects_list: bool = False
    required: list[str]
    elements: list[FormElementRecord]
