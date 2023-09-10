from typing import Any

from .abstract_limit_validator import AbstractIntLimitValidator, Number


class MinLengthValidator(AbstractIntLimitValidator):

    def _get_error_message(self, limit_value: Number) -> str:
        return f"Ensure this value has at least {limit_value} elements."

    def _clean(self, value: Any) -> Number:
        return len(value)

    def _check_if_valid(self, limit_value: Number, cleaned_value: Number) -> bool:
        return cleaned_value >= limit_value
