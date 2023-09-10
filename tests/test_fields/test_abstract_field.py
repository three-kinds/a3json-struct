# -*- coding: utf-8 -*-
import unittest
import random

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test__str(self):
        self.assertIn('CharField', str(struct.CharField()))

        class User(struct.JsonStruct):
            name = struct.CharField()

        self.assertEqual('User.name', str(User.get_fields()['name']))

    def test__clean(self):
        class User(struct.JsonStruct):
            name = struct.CharField(required=False)

        user = User()
        user.full_clean()

        self.assertEqual(user.name, None)

    def test__default__success(self):
        class User(struct.JsonStruct):
            name = struct.CharField(default='anonymous')
            age = struct.IntegerField(default=lambda: random.randint(10, 40))

        user = User()
        user.full_clean()

        self.assertIsNotNone(user.name)
        self.assertGreaterEqual(user.age, 10)

    def test__default__failed(self):
        class User(struct.JsonStruct):
            name = struct.CharField(required=True)

        user = User()
        with self.assertRaises(errors.ValidationError):
            user.full_clean()
