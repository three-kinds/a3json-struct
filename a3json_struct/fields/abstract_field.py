import abc
from typing import Any, Callable, List, Type, Tuple

from a3json_struct.errors import ValidationError
from .utils import set_nonempty_kv


class AbstractField(abc.ABC):
    def __init__(
        self,
        verbose_name: str | None = None,
        default: Any = None,
        required: bool = True,
        validators: List[Callable] | None = None,
        description: str | None = None,
    ):
        self._verbose_name = verbose_name
        self._default = default
        self._required = required
        self._validators = validators or list()
        self._description = description
        # struct
        self._struct_kls: Type | None = None
        self._name: str | None = None

    def __str__(self) -> str:
        if self._struct_kls is None:
            return super().__str__()
        else:
            return f"{self._struct_kls.__name__}.{self._name}"

    def contribute_to_struct(self, struct_kls: Type, name: str):
        self._struct_kls = struct_kls
        self._name = name
        if self._verbose_name is None:
            self._verbose_name = name

    def _validate(self, value: Any) -> Any:
        if value is None and self._default is not None:
            if callable(self._default):
                value = self._default()
            else:
                value = self._default

        if value is None and self._required:
            raise ValidationError("This field is required.")

        return value

    def _run_validators(self, value: Any):
        for v in self._validators:
            v(value)

    def clean(self, value: Any) -> Any:
        value = self._validate(value)
        if value is None:
            return

        value = self._cast_to_python(value)

        self._run_validators(value)
        return value

    @abc.abstractmethod
    def _cast_to_python(self, value: Any) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def _cast_to_json(self, cleaned_value: Any) -> Any:
        raise NotImplementedError()

    def _cast_to_bson(self, cleaned_value: Any) -> Any:
        return self._cast_to_json(cleaned_value)

    def to_json(self, cleaned_value: Any) -> Any:
        if cleaned_value is None:
            return
        else:
            return self._cast_to_json(cleaned_value)

    def to_bson(self, cleaned_value: Any) -> Any:
        if cleaned_value is None:
            return
        else:
            return self._cast_to_bson(cleaned_value)

    def is_required(self) -> bool:
        return self._required

    @abc.abstractmethod
    def _get_json_type_and_openapi_format(self) -> Tuple[str, str]:
        raise NotImplementedError()

    def generate_openapi_object(self) -> dict:
        json_type, openapi_format = self._get_json_type_and_openapi_format()
        od = {
            "type": json_type,
            "format": openapi_format,
        }

        set_nonempty_kv(od, "title", self._verbose_name)
        set_nonempty_kv(od, "description", self._description)

        if self._default is not None:
            if callable(self._default):
                value = self._default()
            else:
                value = self._default

            od["default"] = self.to_json(value)

        return od

    def generate_meta_object(self) -> dict:
        # It is used only for simple verification, so it's not support custom validators or default.
        return {
            "class_name": self.__class__.__name__,
            "verbose_name": self._verbose_name,
            "required": self._required,
            "description": self._description,
        }
