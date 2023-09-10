import abc
from typing import Any, Union
from decimal import Decimal

from a3json_struct.errors import ValidationError


Number = Union[float, int, Decimal]


class AbstractIntLimitValidator(abc.ABC):

    def __init__(self, limit_value: Number):
        self._limit_value = limit_value

    @abc.abstractmethod
    def _clean(self, value: Any) -> Number:
        raise NotImplementedError()

    @abc.abstractmethod
    def _check_if_valid(self, limit_value: Number, cleaned_value: Number) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_error_message(self, limit_value: Number) -> str:
        raise NotImplementedError()

    def __call__(self, value: Any):
        cleaned_value = self._clean(value)
        if not self._check_if_valid(self._limit_value, cleaned_value):
            raise ValidationError(self._get_error_message(self._limit_value))
