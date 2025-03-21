# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__cast_to_python(self):
        class User(struct.JsonStruct):
            birthday = struct.DateField()

        user = User()
        user.birthday = "20a2-10-01"
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.birthday = "2020-01-10"
        user.full_clean()
