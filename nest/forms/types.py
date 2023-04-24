from __future__ import annotations

from typing import Any, TypedDict

from nest.frontend.components import FrontendComponents


class JSONSchemaProperties(TypedDict, total=False):
    """
    The property dict only generates values that are populated, so None values will
    not be a part of the returned schema.
    """

    title: str
    type: str | None
    default: Any
    description: str
    enum: list[Any]
    allOf: list[dict[str, str]]
    alias: str  # The public name of the field,
    const: Any  # Field is required and *must* take its default value

    # Ints:
    maximum: int  # Requires field to be "less than or equal to" (le param).
    minimum: int  # Requires field to be "greater than or equal to" (ge param).
    exclusiveMinimum: int  # Requires the field to be "greater than" (gt param).
    exclusiveMaximum: int  # Requires the field to be "less than" (lt param).
    multipleOf: float  # Requires the field to be "a multiple of" (modulus).

    # Lists:
    minItems: int  # Requires field (list) to have a minimum number of elements.
    maxItems: int  # Requires field (list) to have a maximum number of elements.
    uniqueItems: bool  # Requires field (list) not to have duplicated elements.

    # Strings:
    minLength: int  # Requires field (str) to have a minimum length.
    maxLength: int  # Requires field (str) to have a maximum length.
    pattern: str  # Requires field (str) match against a regex pattern string.

    # Custom:
    parent: str | None
    component: FrontendComponents | None
    placeholder: str
    help_text: str
    hidden_label: bool
    col_span: int
    section: str


class JSONSchema(TypedDict, total=False):
    title: str
    description: str
    type: str
    required: list[str]
    properties: dict[str, JSONSchemaProperties | str]
    definitions: dict[str, JSONSchema | JSONSchemaProperties]
