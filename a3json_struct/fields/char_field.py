from typing import Any, Set, Tuple
from a3json_struct.errors import ValidationError
from a3json_struct import validators

from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat, set_nonempty_kv


class CharField(AbstractField):
    def __init__(
        self,
        min_length: int | None = None,
        max_length: int | None = None,
        choices: Set[str] | None = None,
        pattern: str | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._min_length = min_length
        self._max_length = max_length
        self._choices = choices
        self._pattern = pattern

        if self._min_length is not None:
            self._validators.append(validators.MinLengthValidator(self._min_length))
        if self._max_length is not None:
            self._validators.append(validators.MaxLengthValidator(self._max_length))
        if self._pattern is not None:
            self._validators.append(validators.RegexValidator(self._pattern))

    def _validate(self, value: Any) -> Any:
        value = super()._validate(value)
        if self._choices is not None and value is not None and value not in self._choices:
            raise ValidationError(f'Value "{value}" is not a valid choice.')
        return value

    def _cast_to_python(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        else:
            return str(value)

    def _cast_to_json(self, cleaned_value: str) -> str:
        return cleaned_value

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.String, OpenAPIFormat.String

    def generate_openapi_object(self) -> dict:
        od = super().generate_openapi_object()

        set_nonempty_kv(od, "minLength", self._min_length)
        set_nonempty_kv(od, "maxLength", self._max_length)
        set_nonempty_kv(od, "pattern", self._pattern)

        if self._choices is not None:
            od["enum"] = list(self._choices)

        return od

    def generate_meta_object(self) -> dict:
        od = super().generate_meta_object()

        od["min_length"] = self._min_length
        od["max_length"] = self._max_length
        od["choices"] = list(self._choices) if self._choices is not None else None
        od["pattern"] = self._pattern

        return od
