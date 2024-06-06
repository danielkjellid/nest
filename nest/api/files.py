from ninja.files import UploadedFile as NinjaUploadedFile

from pydantic_core import core_schema
from pydantic.json_schema import GetJsonSchemaHandler, JsonSchemaValue


class UploadedFile(NinjaUploadedFile):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        print(json_schema)
        json_schema.update(
            type="string",
            format="binary",
            # placeholder=f"Upload {core_schema.name.lower()}",
        )


class UploadedImageFile(NinjaUploadedFile):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        print(json_schema)
        json_schema.update(
            type="string",
            format="binary",
            # placeholder=f"Upload {core_schema.name.lower()}",
        )
