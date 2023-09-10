# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test__validators(self):
        class User(struct.JsonStruct):
            money = struct.DecimalField(min_value=Decimal(0), max_value=Decimal(10))

        user = User()
        user.money = -1
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.money = 11
        with self.assertRaises(errors.ValidationError):
            user.full_clean()

        user.money = 5
        user.full_clean()

        # invalid
        user.money = 'abc'
        with self.assertRaises(errors.ValidationError):
            user.full_clean()
