# a3json-struct

* describe json struct with python class

## Install

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
    video.comment_list =[
        comment, # instance
        {"content": "content", "post_time": datetime.now()} # or dict
    ]
    
    video.full_clean() # clean instance (the step can be omitted)
    video.to_json()    # return json dict

```
