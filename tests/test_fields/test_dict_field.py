# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):
    def test__cast_to_python(self):
        class Book(struct.JsonStruct):
            attrs = struct.DictField()

        book = Book()

        # failed
        book.attrs = "attrs"
        with self.assertRaises(errors.ValidationError):
            book.full_clean()

        # success
        book.attrs = {"price": 100, "isbn": "12345"}
        book.full_clean()

        # json
        d = book.to_json()
        self.assertEqual(d["attrs"], book.attrs)
