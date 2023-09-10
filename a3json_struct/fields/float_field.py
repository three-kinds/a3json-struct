from typing import Any

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField


class FloatField(AbstractField):

    def _cast_to_python(self, value: Any) -> float:
        if isinstance(value, float):
            return value

        try:
            return float(str(value))
        except (TypeError, ValueError):
            raise ValidationError(f'Value "{value}" is not a valid float number.')

    def to_json(self, cleaned_value: float) -> float:
        return cleaned_value
