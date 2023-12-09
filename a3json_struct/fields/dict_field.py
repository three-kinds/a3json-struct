from typing import Any

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField


class DictField(AbstractField):

    def _cast_to_python(self, value: Any) -> dict:
        if isinstance(value, dict):
            return value

        raise ValidationError(f'Value "{value}" is not a valid dict.')

    def _cast_to_json(self, cleaned_value: dict) -> dict:
        return cleaned_value
