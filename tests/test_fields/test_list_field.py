# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__validators(self):
        class User(struct.JsonStruct):
            hobbies = struct.ListField(element_field=struct.CharField(), min_length=1, max_length=3, unique=True)

        user = User()
        user.hobbies = list()
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.hobbies = ["1", "2", "3", "4"]
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.hobbies = [1, 2, 3]
        user.full_clean()

        # cast_to_python
        user.hobbies = [
            0,
            1,
            None,
        ]
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()
        self.assertIn("hobbies[2]", str(e.exception))

        user.hobbies = 123
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        # unique
        user.hobbies = [
            1,
            1,
            2,
        ]
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()
        self.assertIn("hobbies[1]", str(e.exception))
