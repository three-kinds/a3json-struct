# -*- coding: utf-8 -*-
import re
from a3json_struct.errors import ValidationError


class RegexValidator:
    _pattern = ""
    _flags = 0
    _inverse_match = False
    _error_message = "Enter a valid value."

    def __init__(self, pattern: str = None, flags: int = None, inverse_match: bool = None, error_message: str = None):
        if pattern is not None:
            self._pattern = pattern
        if flags is not None:
            self._flags = flags
        if inverse_match is not None:
            self._inverse_match = inverse_match
        if error_message is not None:
            self._error_message = error_message

        self._compiled_regex = re.compile(self._pattern, self._flags)

    def __call__(self, value: str):
        regex_matches = self._compiled_regex.search(value)
        is_invalid = regex_matches is None
        if self._inverse_match:
            is_invalid = not is_invalid

        if is_invalid:
            raise ValidationError(self._error_message)
