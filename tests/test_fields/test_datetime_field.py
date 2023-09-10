# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test__cast_to_python(self):
        class User(struct.JsonStruct):
            join_time = struct.DateTimeField()

        user = User()
        user.join_time = '2022-13-01 10:10:11'
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.join_time = '2022-12-01 10:10:11'
        user.full_clean()
