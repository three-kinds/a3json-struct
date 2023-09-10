from typing import Any

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField


class BooleanField(AbstractField):

    def _cast_to_python(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value

        value = str(value).lower()

        if value in ('t', 'true', '1'):
            return True

        if value in ('f', 'false', '0'):
            return False

        raise ValidationError(f'Value "{value}" is not a valid boolean.')

    def _cast_to_json(self, cleaned_value: bool) -> bool:
        return cleaned_value
