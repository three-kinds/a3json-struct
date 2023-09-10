# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors, validators


class T(unittest.TestCase):

    def test__inverse_match(self):
        error_message = "Please use better password."

        class User(struct.JsonStruct):
            password = struct.CharField(validators=[validators.RegexValidator(
                pattern='12345', flags=0, inverse_match=True, error_message=error_message
            )])

        user = User()
        user.password = "123456"
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()
        self.assertIn(error_message, str(e.exception))

        user.password = "abc123"
        user.full_clean()
