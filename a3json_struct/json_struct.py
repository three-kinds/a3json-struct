from typing import Dict, Any
import copy

from a3json_struct.errors import ValidationError
from a3json_struct.fields.abstract_field import AbstractField


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
            for kls in mro_structs[1: -2]:
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
        new_cls._fields = fields
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
        self._super_setattr('_has_full_clean', v)

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
