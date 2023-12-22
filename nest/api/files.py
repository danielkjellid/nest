from typing import Any

from ninja.files import UploadedFile as NinjaUploadedFile
from pydantic.fields import ModelField


class UploadedFile(NinjaUploadedFile):
    @classmethod
    # TODO[pydantic]: We couldn't refactor `__modify_schema__`, please create the `__get_pydantic_json_schema__` manually.
    # Check https://docs.pydantic.dev/latest/migration/#defining-custom-types for more information.
    def __modify_schema__(
        cls, field_schema: dict[str, Any], field: ModelField | None
    ) -> None:
        if field:
            field_schema.update(
                type="string",
                format="binary",
                placeholder=f"Upload {field.name.lower()}",
            )


class UploadedImageFile(NinjaUploadedFile):
    @classmethod
    # TODO[pydantic]: We couldn't refactor `__modify_schema__`, please create the `__get_pydantic_json_schema__` manually.
    # Check https://docs.pydantic.dev/latest/migration/#defining-custom-types for more information.
    def __modify_schema__(
        cls, field_schema: dict[str, Any], field: ModelField | None
    ) -> None:
        if field:
            field_schema.update(
                type="string",
                format="binary",
                placeholder=f"Upload {field.name.lower()}",
            )
