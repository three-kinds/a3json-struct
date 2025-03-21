# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__cast_to_python(self):
        class SubStruct(struct.JsonStruct):
            sub_name = struct.CharField(min_length=3)

        class User(struct.JsonStruct):
            sub = struct.ObjectField(obj_kls=SubStruct)

        user = User()
        user.sub = {"sub_name": "a" * 2}
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()
        self.assertIn("sub.sub_name:", str(e.exception))

        user = User()
        user.sub = lambda x: {"sub_name": "a" * 3}
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.sub = {"sub_name": "a" * 3}
        user.full_clean()
