# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__validators(self):
        class User(struct.JsonStruct):
            name = struct.CharField(min_length=3, max_length=8, pattern="aaa")

        user = User()
        user.name = "a" * 2
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.name = "a" * 10
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.name = "aabb"
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.name = "aaabbb"
        user.full_clean()

    def test__choices(self):
        male = "male"
        female = "female"

        class User(struct.JsonStruct):
            gender = struct.CharField(choices={male, female})

        user = User()
        user.gender = female
        user.full_clean()

        user.gender = "xxx"
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()
        self.assertIn("choice", str(e.exception))

    def test__cast_to_python(self):
        class User(struct.JsonStruct):
            name = struct.CharField()

        user = User()
        user.name = 1
        user.full_clean()
        self.assertEqual(user.name, "1")
