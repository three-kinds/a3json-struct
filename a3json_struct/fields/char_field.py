from typing import Any, Set
from a3json_struct.errors import ValidationError
from a3json_struct import validators

from .abstract_field import AbstractField


class CharField(AbstractField):

    def __init__(
            self,
            min_length: int = None,
            max_length: int = None,
            choices: Set[str] = None,
            pattern: str = None,
            *args, **kwargs
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
