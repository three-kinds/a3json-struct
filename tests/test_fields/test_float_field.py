# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__validators(self):
        class User(struct.JsonStruct):
            height_m = struct.FloatField(min_value=0.0, max_value=2.5)

        user = User()
        user.height_m = -1
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.height_m = 3
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.height_m = 1.8
        user.full_clean()

        # invalid
        user.height_m = "abc"
        with self.assertRaises(errors.ValidationError):
            user.full_clean()
