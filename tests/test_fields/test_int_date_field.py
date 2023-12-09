# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test__cast_to_python(self):
        class User(struct.JsonStruct):
            birthday = struct.IntDateField()

        user = User()
        user.birthday = 21001
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.birthday = 20200110
        user.full_clean()

        user.birthday = '20a2-10-01'
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.birthday = '2020-01-10'
        user.full_clean()

    def test__cast_to_json(self):
        class User(struct.JsonStruct):
            birthday = struct.IntDateField()

        user = User(birthday='2020-01-10')
        d = user.to_json()
        self.assertEqual(d['birthday'], 20200110)
