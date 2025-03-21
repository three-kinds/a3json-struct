# -*- coding: utf-8 -*-
import datetime
import unittest
from decimal import Decimal

from a3json_struct import struct, errors
from a3json_struct.fields.utils import JsonType


class T(unittest.TestCase):
    def test_simple_struct(self):
        class User(struct.JsonStruct):
            username = struct.CharField()
            age = struct.IntegerField()
            updated_time = struct.DateTimeField(required=False)

        user = User(username="username")
        user.age = 13
        user.updated_time = "2021-02-01T00:00:01"
        # to_json
        rd = user.to_bson()
        self.assertTrue(isinstance(rd["updated_time"], datetime.datetime))

        user.updated_time = datetime.date.today()
        user.full_clean()
        self.assertTrue(isinstance(user.updated_time, datetime.datetime))

        user.updated_time = "2021-02-01"
        user.full_clean()
        self.assertTrue(isinstance(user.updated_time, datetime.datetime))

        # to_json
        rd = user.to_json()

        self.assertNotIn("not-clean", str(user))
        self.assertEqual(rd["username"], user.username)
        self.assertEqual(rd["age"], user.age)

        # clean
        user.age = "abc"
        self.assertIn("not-clean", str(user))
        with self.assertRaises(errors.ValidationError) as e:
            user.full_clean()

        self.assertIn("age", str(e.exception))
        # generate_openapi_schema
        sd = User.generate_openapi_schema()
        self.assertEqual(sd["type"], JsonType.Object)
        self.assertIn("username", sd["required"])

        self.assertIn("username", sd["properties"])
        self.assertIn("age", sd["properties"])
        # generate_meta
        sd = User.generate_meta_schema()
        self.assertIn("username", sd["fields"])
        self.assertIn("age", sd["fields"])

        # build
        user_class = struct.JsonStruct.build_variant_from_meta_schema(sd)
        user = user_class()
        user.username = "username"
        user.age = 13
        rd = user.to_bson()
        self.assertEqual(rd["updated_time"], None)
        rd = user.to_json()

        self.assertNotIn("not-clean", str(user))
        self.assertEqual(rd["username"], user.username)
        self.assertEqual(rd["age"], user.age)

        with self.assertRaises(errors.ValidationError):
            user_class(age="abc", username="aha").full_clean()

    def test_complex_struct(self):
        class User(struct.JsonStruct):
            name = struct.CharField(min_length=1)

        class Comment(struct.JsonStruct):
            user = struct.ObjectField(obj_kls=User)
            content = struct.CharField()
            post_time = struct.DateTimeField()

        class Video(struct.JsonStruct):
            id = struct.IntegerField(verbose_name="video id")
            title = struct.CharField(min_length=5, max_length=30)
            rate = struct.FloatField()
            score = struct.DecimalField()
            author = struct.ObjectField(obj_kls=User)
            tag_list = struct.ListField(element_field=struct.CharField(min_length=2, max_length=8), required=False)
            comment_list = struct.ListField(element_field=struct.ObjectField(obj_kls=Comment))
            highlight_list = struct.ListField(
                element_field=struct.ListField(element_field=struct.IntegerField(min_value=0))
            )

        # generate_meta
        sd = Video.generate_meta_schema()
        # build
        video_class = struct.JsonStruct.build_variant_from_meta_schema(sd)
        video = video_class()
        video.id = 1
        video.title = "title"
        video.author = {"name": "author"}
        video.tag_list = [
            "a-tag",
            "b-tag",
            "c-tag",
        ]
        video.rate = 1.0
        video.score = 5
        video.comment_list = [{"user": {"name": "commenter"}, "content": "content", "post_time": "2024-01-21 17:57:00"}]
        video.highlight_list = [[1, 2], [3, 4]]
        video.full_clean()

        video.comment_list = [{"user": {"name": ""}, "content": "content", "post_time": "2024-01-21 17:57:00"}]
        with self.assertRaises(errors.ValidationError) as e:
            video.full_clean()

        self.assertIn("comment_list[0].user.name", str(e.exception))

    def test_inherit(self):
        class Animal(struct.JsonStruct):
            name = struct.CharField()

        class Product(struct.JsonStruct):
            price = struct.DecimalField()

        class Displayable:
            name: str  # type: ignore

            def display(self) -> str:
                return self.name

        class Fish(Animal, Product, Displayable):
            pass

        fish = Fish()
        fish.name = "fish"
        fish.price = "19.9"

        rd = fish.to_json()
        self.assertEqual(rd["name"], fish.name)
        self.assertEqual(fish.display(), fish.name)
        self.assertEqual(Decimal(rd["price"]), fish.price)
