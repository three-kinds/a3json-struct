# -*- coding: utf-8 -*-
import unittest
from a3json_struct import errors


class T(unittest.TestCase):
    def test__str(self):
        message = "message"
        e = errors.ValidationError(message)
        self.assertEqual(str(e), message)
        # set field
        field = "field"
        e.set_field(field)
        self.assertEqual(str(e), f"{field}: {message}")
        # set index
        e = errors.ValidationError(message)
        index0 = 0
        index1 = 1
        e.set_index(index0)
        e.set_index(index1)
        e.set_field(field)
        self.assertEqual(str(e), f"{field}[{index1}][{index0}]: {message}")
