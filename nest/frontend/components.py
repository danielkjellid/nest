from enum import Enum

from nest.api.openapi import add_to_openapi_schema


@add_to_openapi_schema
class FrontendComponents(Enum):
    AUTOCOMPLETE = "Autocomplete"
    CHECKBOX = "Checkbox"
    CHIP = "Chip"
    COLOR_INPUT = "ColorInput"
    FILE_INPUT = "FileInput"
    MULTISELECT = "MultiSelect"
    NUMBER_INPUT = "NumberInput"
    PASSWORD_INPUT = "PasswordInput"
    PIN_INPUT = "PinInput"
    RADIO = "Radio"
    RATING = "Rating"
    SELECT = "Select"
    SLIDER = "Slider"
    SWITCH = "Switch"
    TEXT_AREA = "Textarea"
    TEXT_INPUT = "TextInput"
