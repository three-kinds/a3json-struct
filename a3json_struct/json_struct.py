from typing import Dict, Any, Type
import copy

from a3py.practical.dynamic import find_all_subclasses
from a3py.simplified.case import snake2camel
from a3json_struct.errors import ValidationError
from a3json_struct.fields.abstract_field import AbstractField
from a3json_struct.fields.utils import JsonType


class JsonStructMetaClass(type):
    def __new__(mcs, name, bases, attrs: dict, **kwargs):
        # exclude self
        parents = [b for b in bases if isinstance(b, JsonStructMetaClass)]
        if not parents:
            return super().__new__(mcs, name, bases, attrs, **kwargs)

        # `field_name_set`: subclass's field first, if parent class has the same field, it will be ignored
        field_name_set = set()
        fields = dict()
        for field_name, field_instance in attrs.items():
            field_name_set.add(field_name)

            if isinstance(field_instance, AbstractField):
                fields[field_name] = field_instance

        # pop the fields of current class
        for field_name in fields.keys():
            attrs.pop(field_name)

        # new class
        new_cls = super().__new__(mcs, name, bases, attrs, **kwargs)

        # parent fields
        mro_structs = new_cls.mro()
        if len(mro_structs) > 3:
            parent_structs = list()
            for kls in mro_structs[1:-2]:
                if issubclass(kls, JsonStruct) and kls != JsonStruct:
                    parent_structs.append(kls)

            for parent in parent_structs:
                parent_fields = parent.get_fields()

                for name, field in parent_fields.items():
                    new_field = copy.deepcopy(field)
                    if name not in field_name_set:
                        fields[name] = new_field
                        field_name_set.add(name)

        # bind to class
        for field_name, field_instance in fields.items():
            field_instance.contribute_to_struct(new_cls, field_name)

        # set private _fields
        setattr(new_cls, "_fields", fields)
        return new_cls


class JsonStruct(metaclass=JsonStructMetaClass):
    _fields: Dict[str, AbstractField]
    _has_full_clean: bool

    @classmethod
    def get_fields(cls) -> Dict[str, AbstractField]:
        return cls._fields

    def __init__(self, **kwargs):
        self._set_has_full_clean(False)

        field_name_list = list()
        for field_name, field_instance in self.get_fields().items():
            field_name_list.append(field_name)
            self._super_setattr(field_name, None)

        for k, v in kwargs.items():
            if k in field_name_list:
                setattr(self, k, v)

    def _super_setattr(self, name: str, value: Any):
        super().__setattr__(name, value)

    def _set_has_full_clean(self, v: bool):
        self._super_setattr("_has_full_clean", v)

    def __setattr__(self, name: str, value: Any):
        self._super_setattr(name, value)

        if self._has_full_clean:
            self._set_has_full_clean(False)

    def __str__(self) -> str:
        name = self.__class__.__name__
        if not self._has_full_clean:
            name = f"{name}['not-clean']"
        return name

    def _clean_fields(self):
        for field_name, field_instance in self.get_fields().items():
            value = getattr(self, field_name, None)

            try:
                value = field_instance.clean(value)
            except ValidationError as e:
                e.set_field(field_name)
                raise e

            value = field_instance.clean(value)
            setattr(self, field_name, value)

    def _clean_struct(self):
        # for custom override
        pass

    def full_clean(self):
        self._clean_fields()
        self._clean_struct()
        self._set_has_full_clean(True)

    def to_json(self) -> dict:
        if not self._has_full_clean:
            self.full_clean()

        rd = dict()
        for field_name, field_instance in self.get_fields().items():
            value = getattr(self, field_name, None)
            rd[field_name] = field_instance.to_json(value)

        return rd

    def to_bson(self) -> dict:
        if not self._has_full_clean:
            self.full_clean()

        rd = dict()
        for field_name, field_instance in self.get_fields().items():
            value = getattr(self, field_name, None)
            rd[field_name] = field_instance.to_bson(value)

        return rd

    @classmethod
    def generate_openapi_schema(cls) -> dict:
        required_list = list()
        properties = dict()

        for field_name, field_instance in cls.get_fields().items():
            if field_instance.is_required():
                required_list.append(field_name)

            properties[field_name] = field_instance.generate_openapi_object()

        return {
            "type": JsonType.Object,
            "properties": properties,
            "required": required_list,
        }

    @classmethod
    def generate_meta_schema(cls) -> dict:
        fields = dict()

        for field_name, field_instance in cls.get_fields().items():
            fields[field_name] = field_instance.generate_meta_object()

        return {"fields": fields}

    @classmethod
    def build_variant_from_meta_schema(
        cls, schema: Dict[str, Dict], class_name: str | None = None
    ) -> Type["JsonStruct"]:
        schema = copy.deepcopy(schema)
        fields = dict()
        for field_name, meta_object in schema["fields"].items():
            instance = _get_field_instance_by_meta(cls, meta_object)
            fields[field_name] = instance

        class_name = class_name or "Variant"
        # noinspection PyTypeChecker
        variant: Type["JsonStruct"] = type(class_name, (cls,), dict())
        setattr(variant, "_fields", fields)
        return variant


_all_inner_fields_classes: Dict[str, Type] = dict()


def _get_all_inner_field_class() -> Dict:
    if len(_all_inner_fields_classes) == 0:
        field_class_list = find_all_subclasses("a3json_struct.struct", AbstractField)
        for field_class in field_class_list:
            _all_inner_fields_classes[field_class.__name__] = field_class

    return _all_inner_fields_classes


def _get_field_instance_by_meta(base: Type["JsonStruct"], meta_object: dict) -> AbstractField:
    inner_classes = _get_all_inner_field_class()

    class_name = meta_object.pop("class_name")
    field_class = inner_classes.get(class_name)
    assert field_class is not None, f"Unknown inner field class: {class_name}"

    if class_name == "ListField":
        element_field_meta = meta_object.pop("element_field_meta")
        meta_object["element_field"] = _get_field_instance_by_meta(base, element_field_meta)
    elif class_name == "ObjectField":
        obj_kls_meta = meta_object.pop("obj_kls_meta")
        obj_kls_name = meta_object.pop("obj_kls_name")
        meta_object["obj_kls"] = base.build_variant_from_meta_schema(obj_kls_meta, class_name=snake2camel(obj_kls_name))

    instance = field_class(**meta_object)
    return instance
