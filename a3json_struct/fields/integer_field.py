from typing import Any, Set
from a3json_struct.errors import ValidationError
from a3json_struct import validators

from .abstract_field import AbstractField


class IntegerField(AbstractField):

    def __init__(
            self,
            min_value: int = None,
            max_value: int = None,
            choices: Set[int] = None,
            *args, **kwargs
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
