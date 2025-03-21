from typing import Any, Tuple
import datetime

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat


class DateTimeField(AbstractField):
    def _cast_to_python(self, value: Any) -> datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, datetime.date):
            return datetime.datetime(year=value.year, month=value.month, day=value.day)

        try:
            return datetime.datetime.fromisoformat(str(value))
        except ValueError:
            raise ValidationError(
                f'Value "{value}" must has the correct format (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])，"'
                f"and must be a valid datetime."
            )

    def _cast_to_json(self, cleaned_value: datetime.datetime) -> str:
        return cleaned_value.isoformat()

    def _cast_to_bson(self, cleaned_value: datetime.datetime) -> Any:
        return cleaned_value

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.String, OpenAPIFormat.Date
