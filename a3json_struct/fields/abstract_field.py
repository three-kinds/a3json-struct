import abc
from typing import Any, Callable, List, Type

from a3json_struct.errors import ValidationError


class AbstractField(abc.ABC):

    def __init__(
            self,
            verbose_name: str = None,
            default: Any = None,
            required: bool = True,
            validators: List[Callable] = None
    ):
        self._verbose_name = verbose_name
        self._default = default
        self._required = required
        self._validators = validators or list()
        # struct
        self._struct_kls = None
        self._name = None

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
            if isinstance(self._default, Callable):
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

    def to_json(self, cleaned_value: Any) -> Any:
        if cleaned_value is None:
            return
        else:
            return self._cast_to_json(cleaned_value)
