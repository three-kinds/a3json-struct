from typing import Any
from decimal import Decimal, DecimalException

from a3json_struct.errors import ValidationError
from a3json_struct import validators
from .abstract_field import AbstractField


class DecimalField(AbstractField):

    def __init__(
            self,
            min_value: Decimal = None,
            max_value: Decimal = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._min_value = min_value
        self._max_value = max_value

        if self._min_value is not None:
            self._validators.append(validators.MinValueValidator(self._min_value))
        if self._max_value is not None:
            self._validators.append(validators.MaxValueValidator(self._max_value))

    def _cast_to_python(self, value: Any) -> Decimal:
        if isinstance(value, Decimal):
            return value

        try:
            return Decimal(str(value))
        except DecimalException:
            raise ValidationError(f'Value "{value}" is not a valid decimal number.')

    def _cast_to_json(self, cleaned_value: Decimal) -> str:
        return str(cleaned_value)
