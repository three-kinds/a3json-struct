# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct


class T(unittest.TestCase):

    def test__all_fields__success(self):
        class SubStruct(struct.JsonStruct):
            sub_name = struct.CharField()

        class AllFieldsStruct(struct.JsonStruct):
            boolean_field = struct.BooleanField()
            char_field = struct.CharField()
            date_field = struct.DateField()
            datetime_field = struct.DateTimeField()
            decimal_field = struct.DecimalField()
            float_field = struct.FloatField()
            integer_field = struct.IntegerField()
            list_field = struct.ListField(element_field=struct.IntegerField())
            object_field = struct.ObjectField(obj_kls=SubStruct)

        afs = AllFieldsStruct()
        afs.boolean_field = True
        afs.char_field = "string"
        afs.date_field = "2020-01-01"
        afs.datetime_field = "2020-01-01T00:00:00.305823+00:00"
        afs.decimal_field = '2.1'
        afs.float_field = 2.1
        afs.integer_field = 2
        afs.list_field = [1, 2, 3]
        afs.object_field = SubStruct(sub_name="sub_name")

        rd = afs.to_json()
        self.assertIn('boolean_field', rd)
        self.assertIn('char_field', rd)
        self.assertIn('date_field', rd)
        self.assertIn('datetime_field', rd)
        self.assertIn('decimal_field', rd)
        self.assertIn('float_field', rd)
        self.assertIn('integer_field', rd)
        self.assertIn('list_field', rd)
        self.assertIn('object_field', rd)
