from typing import Any, Tuple
import datetime

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat


class DateField(AbstractField):
    def _cast_to_python(self, value: Any) -> datetime.date:
        if isinstance(value, datetime.date):
            return value

        try:
            return datetime.date.fromisoformat(str(value))
        except ValueError:
            raise ValidationError(
                f'Value "{value}" must has the correct format (YYYY-MM-DD)，and must be a valid date.'
            )

    def _cast_to_json(self, cleaned_value: datetime.date) -> str:
        return cleaned_value.isoformat()

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.String, OpenAPIFormat.Date
