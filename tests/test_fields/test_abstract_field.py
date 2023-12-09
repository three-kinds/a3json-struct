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

    def test__generate_openapi_object(self):
        default_name = 'xxx'

        def default_score() -> int:
            return 100

        class User(struct.JsonStruct):
            name = struct.CharField(description='name description', required=False, default=default_name)
            score = struct.IntegerField(default=default_score)

        sd = User.generate_openapi_schema()
        self.assertNotIn('name', sd['required'])
        self.assertIn('score', sd['required'])

        name_od = sd['properties']['name']
        score_od = sd['properties']['score']

        self.assertIn('description', name_od)
        self.assertNotIn('description', score_od)

        self.assertEqual(name_od['default'], default_name)
        self.assertEqual(score_od['default'], default_score())
