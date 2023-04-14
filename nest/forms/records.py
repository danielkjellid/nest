from pydantic import BaseModel, StrictBool, StrictInt, StrictStr
from .elements import FrontendElements


class FormSectionRecord(BaseModel):
    """
    A form section groups different parts (elements) of the form and adds them together
    in a section.

    * title:
        The title of the section, renders a header in the section frontend, unless plain
        is passed.

    * blocks:
        A list of form blocks ids to include in the section.

    * columns:
        Optionally divide the form into multiple columns, taking advantage of using
        colspans adjusting width the width of certain elements. The colspan value itself
        is set directly on the form block.

    * plain:
        Render the blocks in an invisible section.
    """

    title: str
    blocks: list[str]
    columns: int | None = None
    plain: bool | None = False


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
    col_span: int | None = None


class FormRecord(BaseModel):
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
    sections: list[FormSectionRecord]
    elements: list[FormElementRecord]
