# -*- coding: utf-8 -*-
from typing import Any


def set_nonempty_kv(d: dict, key: str, v: Any):
    if v not in [None, ""]:
        d[key] = v


class JsonType:
    Boolean = "boolean"
    String = "string"
    Number = "number"
    Array = "array"
    Object = "object"


class OpenAPIFormat:
    Boolean = "boolean"
    String = "string"
    Date = "date"
    Datetime = "datetime"
    Decimal = "decimal"
    Object = "object"
    Float = "float"
    Long = "long"
    Array = "array"
