# a3json-struct

[English](README.md) | 简体中文

`a3json-struct`可以用基于class的语法来描述JSON struct。

## 1. 简介

* [支持多种数据类型](a3json_struct/fields)
* 可以自定义格式检测
* 可以将类实例导出为json、bson
* 可以导出openapi schema
* 可以将类的属性导出为json描述，可以从json描述还原成类

## 2. 使用

### 安装

```shell
pip install a3json-struct

```

### 样例

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
        comment,  # 可以是对象实例
        {"content": "content", "post_time": datetime.now()}  # 也可以是字典
    ]

    video.full_clean()  # 验证数据 （如果使用to_json或to_bson的话，这个步骤可以省略）
    assert isinstance(video.to_json()["comment_list"][0]["post_time"], str)
    assert isinstance(video.to_bson()["comment_list"][0]["post_time"], datetime)

    openapi_schema = Video.generate_openapi_schema()
    print(openapi_schema)

    meta_schema = Video.generate_meta_schema()
    RestoredVideo = struct.JsonStruct.build_variant_from_meta_schema(meta_schema, "RestoredVideo")
    assert RestoredVideo.generate_meta_schema() == meta_schema

```
