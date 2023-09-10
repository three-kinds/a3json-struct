# -*- coding: utf-8 -*-
from typing import Any, List, Iterable
from a3json_struct.errors import ValidationError
from a3json_struct import validators

from .abstract_field import AbstractField


class ListField(AbstractField):

    def __init__(
            self,
            element_field: AbstractField,
            unique: bool = False,
            min_length: int = None,
            max_length: int = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._element_field = element_field
        self._unique = unique

        self._min_length = min_length
        self._max_length = max_length
        if self._min_length is not None:
            self._validators.append(validators.MinLengthValidator(self._min_length))
        if self._max_length is not None:
            self._validators.append(validators.MaxLengthValidator(self._max_length))

    def _validate(self, value: Any) -> Any:
        value = super()._validate(value)

        if self._unique and isinstance(value, Iterable):
            all_set = set()
            for i, v in enumerate(value):
                if v in all_set:
                    e = ValidationError(f'Value "{v}" is not unique.')
                    e.set_index(i)
                    raise e
                else:
                    all_set.add(v)

        return value

    def _cast_to_python(self, value: Any) -> List[Any]:
        if not isinstance(value, list):
            raise ValidationError(f'Value "{value}" must be a list.')

        rl = list()
        for i, v in enumerate(value):
            try:
                cleaned_value = self._element_field.clean(v)
            except ValidationError as e:
                e.set_index(i)
                raise e
            rl.append(cleaned_value)

        return rl

    def _cast_to_json(self, cleaned_value_list: List[Any]) -> List[Any]:
        rl = list()
        for cleaned_value in cleaned_value_list:
            v = self._element_field.to_json(cleaned_value)
            rl.append(v)
        return rl
