from typing import Any, Callable, Dict

from ninja.files import UploadedFile as NinjaUploadedFile
from pydantic_core import CoreSchema

from pydantic import BaseModel, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class UploadedFile(NinjaUploadedFile):
    # @classmethod
    # # TODO[pydantic]: We couldn't refactor `__modify_schema__`, please create the `__get_pydantic_json_schema__` manually.
    # # Check https://docs.pydantic.dev/latest/migration/#defining-custom-types for more information.
    # def __modify_schema__(
    #     cls, field_schema: dict[str, Any], field: ModelField | None
    # ) -> None:
    #     if field:
    #         field_schema.update(
    #             type="string",
    #             format="binary",
    #             placeholder=f"Upload {field.name.lower()}",
    #         )
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)

        print(json_schema)
        return json_schema


class UploadedImageFile(NinjaUploadedFile):
    # @classmethod
    # # TODO[pydantic]: We couldn't refactor `__modify_schema__`, please create the `__get_pydantic_json_schema__` manually.
    # # Check https://docs.pydantic.dev/latest/migration/#defining-custom-types for more information.
    # def __modify_schema__(
    #     cls, field_schema: dict[str, Any], field: ModelField | None
    # ) -> None:
    #     if field:
    #         field_schema.update(
    #             type="string",
    #             format="binary",
    #             placeholder=f"Upload {field.name.lower()}",
    #         )
    ...
