from typing import Any
import datetime

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField


class DateTimeField(AbstractField):

    def _cast_to_python(self, value: Any) -> datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value

        try:
            return datetime.datetime.fromisoformat(str(value))
        except ValueError:
            raise ValidationError(
                f'Value "{value}" must has the correct format (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])，"'
                f'and must be a valid datetime.'
            )

    def _cast_to_json(self, cleaned_value: datetime.datetime) -> str:
        return cleaned_value.isoformat()
