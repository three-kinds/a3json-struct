from typing import Any, Tuple
import datetime

from a3json_struct.errors import ValidationError
from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat


INT_DATE_FORMAT = "%Y%m%d"


class IntDateField(AbstractField):
    def _cast_to_python(self, value: Any) -> datetime.date:
        if isinstance(value, datetime.date):
            return value

        elif isinstance(value, int):
            try:
                return datetime.datetime.strptime(str(value), INT_DATE_FORMAT)
            except ValueError:
                raise ValidationError(
                    f'Value "{value}" must has the correct format ({INT_DATE_FORMAT})，and must be a valid date.'
                )
        else:
            try:
                return datetime.date.fromisoformat(str(value))
            except ValueError:
                raise ValidationError(
                    f'Value "{value}" must has the correct format (YYYY-MM-DD)，and must be a valid date.'
                )

    def _cast_to_json(self, cleaned_value: datetime.date) -> int:
        return int(cleaned_value.strftime("%Y%m%d"))

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.Number, OpenAPIFormat.Date
