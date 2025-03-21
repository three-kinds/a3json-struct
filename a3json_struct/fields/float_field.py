from typing import Any, Tuple

from a3json_struct.errors import ValidationError
from a3json_struct import validators
from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat


class FloatField(AbstractField):
    def __init__(self, min_value: float | None = None, max_value: float | None = None, *args, **kwargs):
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

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.Number, OpenAPIFormat.Float

    def generate_meta_object(self) -> dict:
        od = super().generate_meta_object()

        od["min_value"] = self._min_value
        od["max_value"] = self._max_value

        return od
