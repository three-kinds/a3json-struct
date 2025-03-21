# -*- coding: utf-8 -*-
from typing import Any, Type, TYPE_CHECKING, Tuple
from a3json_struct.errors import ValidationError

from .abstract_field import AbstractField
from .utils import JsonType, OpenAPIFormat

if TYPE_CHECKING:
    from a3json_struct.json_struct import JsonStruct


class ObjectField(AbstractField):
    def __init__(self, obj_kls: Type["JsonStruct"], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._obj_kls = obj_kls

    def _cast_to_python(self, value: Any) -> "JsonStruct":
        if isinstance(value, dict):
            obj_instance = self._obj_kls(**value)
        elif isinstance(value, self._obj_kls):
            obj_instance = value
        else:
            raise ValidationError(f'Value must be a dict or type {self._obj_kls.__name__}, not "{type(value)}".')

        obj_instance.full_clean()
        return obj_instance

    def _cast_to_json(self, cleaned_value: "JsonStruct") -> dict:
        return cleaned_value.to_json()

    def _cast_to_bson(self, cleaned_value: "JsonStruct") -> dict:
        return cleaned_value.to_bson()

    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        return JsonType.Object, OpenAPIFormat.Object

    def generate_openapi_object(self) -> dict:
        od = super().generate_openapi_object()

        sub_od = self._obj_kls.generate_openapi_schema()
        od.update(sub_od)

        return od

    def generate_meta_object(self) -> dict:
        od = super().generate_meta_object()

        od["obj_kls_meta"] = self._obj_kls.generate_meta_schema()
        od["obj_kls_name"] = self._obj_kls.__name__

        return od
