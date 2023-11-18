from typing import TypedDict, Any, TypeAlias, NotRequired


class EnumDict(TypedDict):
    label: str
    value: str | int


#########
# Paths #
#########


class PathOperationResponseContent(TypedDict):
    schema: dict[str, str]


class PathOperationResponse(TypedDict):
    description: str
    content: dict[str, PathOperationResponseContent]


class PathOperation(TypedDict):
    operation_id: str
    summary: str
    parameters: list[str]
    description: str
    tags: list[str]
    security: list[dict[str, list[Any]]]
    responses: dict[str, PathOperationResponse]


class PathGet(TypedDict):
    get: PathOperation


class PathPost(TypedDict):
    post: PathOperation


class PathPut(TypedDict):
    put: PathOperation


class PathDelete(TypedDict):
    delete: PathOperation


Path: TypeAlias = PathGet | PathPost | PathPut | PathDelete


##############
# Components #
##############

# Properties


class PropertyBase(TypedDict, total=True):
    title: str
    type: NotRequired[str]  # Enum values purposefully leaves the type out.
    allOf: NotRequired[Any]
    anyOf: NotRequired[Any]
    enum: NotRequired[list[EnumDict]]
    format: NotRequired[str]
    items: NotRequired[dict[str, str]]


class PropertyExtra(PropertyBase, total=True):
    help_text: str | None
    component: str | None
    default_value: str | None
    placeholder: str | None
    hidden_label: bool
    col_span: int | None
    order: int
    section: str | None
    default: NotRequired[Any]
    min: int | None
    max: int | None


Property: TypeAlias = PropertyBase | PropertyExtra


# Definitions


class DefinitionBase(TypedDict):
    title: str
    type: str
    required: NotRequired[list[str]]


class DefinitionProperty(DefinitionBase):
    properties: dict[str, PropertyBase | PropertyExtra]


class DefinitionExtra(DefinitionBase):
    columns: int | None


DefinitionEnum = TypedDict(
    "DefinitionEnum",
    {
        "title": str,
        "type": str,
        "required": NotRequired[list[str]],
        "description": str,
        "enum": list[str | int],
        "x-enum-varnames": list[str],
    },
)

Definition: TypeAlias = (
    DefinitionBase | DefinitionProperty | DefinitionExtra | DefinitionEnum
)

ComponentSecurityScheme = TypedDict(
    "ComponentSecurityScheme", {"type": str, "in": str, "name": str}
)


class Component(TypedDict):
    schemas: dict[str, Definition]
    securitySchemes: dict[str, ComponentSecurityScheme]


##########
# Schema #
##########


class SchemaInfo(TypedDict):
    title: str
    version: str
    description: str


class Schema(TypedDict):
    openapi: str  # OpenAPI version
    info: SchemaInfo
    paths: dict[str, Path]
    components: Component
