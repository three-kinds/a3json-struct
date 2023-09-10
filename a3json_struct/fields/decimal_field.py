from typing import Any
from decimal import Decimal, DecimalException

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField


class DecimalField(AbstractField):

    def _cast_to_python(self, value: Any) -> Decimal:
        if isinstance(value, Decimal):
            return value

        try:
            return Decimal(str(value))
        except DecimalException:
            raise ValidationError(f'Value "{value}" is not a valid decimal number.')

    def to_json(self, cleaned_value: Decimal) -> str:
        return str(cleaned_value)
