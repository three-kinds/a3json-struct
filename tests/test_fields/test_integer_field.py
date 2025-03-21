# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__validators(self):
        class User(struct.JsonStruct):
            age = struct.IntegerField(min_value=0, max_value=150)

        user = User()
        user.age = -1
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.age = 250
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.age = 32
        user.full_clean()

        # invalid
        user.age = "abc"
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

    def test__choices(self):
        class User(struct.JsonStruct):
            grade = struct.IntegerField(choices={1, 2, 3, 4, 5, 6})

        user = User()
        user.grade = 100
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.grade = 3
        user.full_clean()
