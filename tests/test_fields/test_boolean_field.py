# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__cast_to_python(self):
        class User(struct.JsonStruct):
            is_active = struct.BooleanField()

        user = User()

        # success
        for v in ["T", "True", "true", "1"]:
            user.is_active = v
            user.full_clean()
            self.assertTrue(user.is_active)

        for v in ["F", "False", "false", "0"]:
            user.is_active = v
            user.full_clean()
            self.assertFalse(user.is_active)

        # failed
        user.is_active = "-a1"
        with self.assertRaises(errors.ValidationError):
            user.full_clean()
