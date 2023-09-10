from typing import Any

from a3json_struct.errors import ValidationError
from a3json_struct import validators
from .abstract_field import AbstractField


class FloatField(AbstractField):
    
    def __init__(
            self,
            min_value: float = None,
            max_value: float = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._min_value = min_value
        self._max_value = max_value

        if self._min_value is not None:
            self._validators.append(validators.MinValueValidator(self._min_value))
        if self._max_value is not None:
            self._validators.append(validators.MaxValueValidator(self._max_value))

    def _cast_to_python(self, value: Any) -> float:
        if isinstance(value, float):
            return value

        try:
            return float(str(value))
        except (TypeError, ValueError):
            raise ValidationError(f'Value "{value}" is not a valid float number.')

    def _cast_to_json(self, cleaned_value: float) -> float:
        return cleaned_value
