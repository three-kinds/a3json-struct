# -*- coding: utf-8 -*-
import unittest

from a3json_struct import struct, errors


class T(unittest.TestCase):

    def test__complex_struct(self):
        class SubStruct(struct.JsonStruct):
            name = struct.CharField(min_length=2)

        class SubComplex(struct.JsonStruct):
            sub_complex = struct.ListField(element_field=struct.ListField(element_field=struct.ObjectField(SubStruct)))

        class Complex(struct.JsonStruct):
            complex = struct.ListField(element_field=struct.ListField(element_field=struct.ObjectField(SubComplex)))

        c = Complex()
        c.complex = [
            [
                {"sub_complex": [[{"name": "00"}]]}, {"sub_complex": [[{"name": "01"}, {"name": 'xx'}]]}
            ],
            [
                {"sub_complex": [[{"name": "10"}]]}, {"sub_complex": [[{"name": "11"}]]}
            ]
        ]
        c.full_clean()

        c.complex[0][1].sub_complex[0][1].name = 'x' # noqa
        with self.assertRaises(errors.ValidationError) as e:
            c.full_clean()
        self.assertIn('complex[0][1].sub_complex[0][1].name', str(e.exception))

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

    def test__all_fields_not_required__success(self):
        class SubStruct(struct.JsonStruct):
            sub_name = struct.CharField()

        class AllFieldsStruct(struct.JsonStruct):
            boolean_field = struct.BooleanField(required=False)
            char_field = struct.CharField(required=False)
            date_field = struct.DateField(required=False)
            datetime_field = struct.DateTimeField(required=False)
            decimal_field = struct.DecimalField(required=False)
            float_field = struct.FloatField(required=False)
            integer_field = struct.IntegerField(required=False)
            list_field = struct.ListField(element_field=struct.IntegerField(), required=False)
            object_field = struct.ObjectField(obj_kls=SubStruct, required=False)
        
        afs = AllFieldsStruct()
        rd = afs.to_json()
        self.assertEqual(rd['boolean_field'], None)
        self.assertEqual(rd['char_field'], None)
        self.assertEqual(rd['date_field'], None)
        self.assertEqual(rd['datetime_field'], None)
        self.assertEqual(rd['decimal_field'], None)
        self.assertEqual(rd['float_field'], None)
        self.assertEqual(rd['integer_field'], None)
        self.assertEqual(rd['list_field'], None)
        self.assertEqual(rd['object_field'], None)
