from .abstract_limit_validator import AbstractIntLimitValidator, Number


class MaxValueValidator(AbstractIntLimitValidator):

    def _clean(self, value: Number) -> Number:
        return value

    def _check_if_valid(self, limit_value: Number, cleaned_value: Number) -> bool:
        return cleaned_value <= limit_value

    def _get_error_message(self, limit_value: Number) -> str:
        return f"Ensure this value is less than or equal to {limit_value}."
