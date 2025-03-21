from typing import Any, Tuple

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat


class DictField(AbstractField):
    def _cast_to_python(self, value: Any) -> dict:
        if isinstance(value, dict):
            return value

        raise ValidationError(f'Value "{value}" is not a valid dict.')

    def _cast_to_json(self, cleaned_value: dict) -> dict:
        return cleaned_value

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.Object, OpenAPIFormat.Object
