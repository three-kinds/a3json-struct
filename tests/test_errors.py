# -*- coding: utf-8 -*-
import unittest
from a3json_struct import errors


class T(unittest.TestCase):

    def test__repr(self):
        e = errors.ValidationError("")
        self.assertIn(errors.ValidationError.__name__, repr(e))
