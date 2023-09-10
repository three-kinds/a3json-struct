# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test_simple_struct(self):
        class User(struct.JsonStruct):
            username = struct.CharField()
            age = struct.IntegerField()

        user = User(username="username")
        user.age = 13

        rd = user.to_json()

        self.assertNotIn("not-clean", str(user))
        self.assertEqual(rd['username'], user.username)
        self.assertEqual(rd['age'], user.age)

        # clean
        user.age = 'abc'
        self.assertIn("not-clean", str(user))
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()

        self.assertIn("age", str(e.exception))

    def test_inherit(self):
        class Animal(struct.JsonStruct):
            name = struct.CharField()

        class Product(struct.JsonStruct):
            price = struct.DecimalField()

        class Displayable:
            name: str

            def display(self):
                return self.name

        class Fish(Animal, Product, Displayable):
            pass

        fish = Fish()
        fish.name = 'fish'
        fish.price = '19.9'

        rd = fish.to_json()
        self.assertEqual(rd['name'], fish.name)
        self.assertEqual(fish.display(), fish.name)
        self.assertEqual(Decimal(rd['price']), fish.price)
