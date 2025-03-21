from typing import Any, Set, Tuple
from a3json_struct.errors import ValidationError
from a3json_struct import validators

from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat, set_nonempty_kv


class IntegerField(AbstractField):
    def __init__(
        self,
        min_value: int | None = None,
        max_value: int | None = None,
        choices: Set[int] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._min_value = min_value
        self._max_value = max_value
        self._choices = choices

        if self._min_value is not None:
            self._validators.append(validators.MinValueValidator(self._min_value))
        if self._max_value is not None:
            self._validators.append(validators.MaxValueValidator(self._max_value))

    def _validate(self, value: Any) -> Any:
        value = super()._validate(value)
        if self._choices is not None and value is not None and value not in self._choices:
            raise ValidationError(f'Value "{value}" is not a valid choice.')
        return value

    def _cast_to_python(self, value: Any) -> int:
        if isinstance(value, int):
            return value

        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValidationError(f'Value "{value}" is not a valid integer number.')

    def _cast_to_json(self, cleaned_value: int) -> int:
        return cleaned_value

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.Number, OpenAPIFormat.Long

    def generate_openapi_object(self) -> dict:
        od = super().generate_openapi_object()

        set_nonempty_kv(od, "minimum", self._min_value)
        set_nonempty_kv(od, "maximum", self._max_value)

        if self._choices is not None:
            od["enum"] = list(self._choices)

        return od

    def generate_meta_object(self) -> dict:
        od = super().generate_meta_object()

        od["min_value"] = self._min_value
        od["max_value"] = self._max_value
        od["choices"] = list(self._choices) if self._choices is not None else None

        return od
