# a3json-struct

English | [简体中文](README_ZH.md)

* `a3json-struct` can describe JSON structs using class-based syntax.

## 1. Introduction

* [Support multiple data type fields](a3json_struct/fields)
* Custom format validators
* Class instances can be exported as JSON, BSON
* The OpenAPI schema can be exported
* The attributes of a class can be exported as a JSON description, and the class can be restored from the JSON description

## 2. Usage

### Install

```shell
pip install a3json-struct

```

## Examples

```python
from datetime import datetime
from a3json_struct import struct


class Comment(struct.JsonStruct):
    content = struct.CharField()
    post_time = struct.DateTimeField()


class Video(struct.JsonStruct):
    id = struct.IntegerField(verbose_name='video id')
    url = struct.CharField()
    title = struct.CharField(min_length=5, max_length=30)
    description = struct.CharField()
    score = struct.DecimalField()
    view_count = struct.IntegerField(default=0)
    tag_list = struct.ListField(element_field=struct.CharField(min_length=2, max_length=8), required=False)
    comment_list = struct.ListField(element_field=struct.ObjectField(obj_kls=Comment))


if __name__ == '__main__':
    comment = Comment()
    comment.content = "content"
    comment.post_time = "2023-09-10 20:32"

    video = Video()
    video.id = 12345
    video.url = "https://xxx.xxx/12345.mp4"
    video.title = "video title"
    video.description = "video description"
    video.score = '2.3'
    video.comment_list = [
        comment,  # It can be an object instance
        {"content": "content", "post_time": datetime.now()}  # or a dictionary
    ]

    video.full_clean()  # Validate data (this step can be omitted if using to_json or to_bson)
    assert isinstance(video.to_json()["comment_list"][0]["post_time"], str)
    assert isinstance(video.to_bson()["comment_list"][0]["post_time"], datetime)

    openapi_schema = Video.generate_openapi_schema()
    print(openapi_schema)

    meta_schema = Video.generate_meta_schema()
    RestoredVideo = struct.JsonStruct.build_variant_from_meta_schema(meta_schema, "RestoredVideo")
    assert RestoredVideo.generate_meta_schema() == meta_schema

```
