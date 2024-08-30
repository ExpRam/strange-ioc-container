# Finally some bad fucking code
import inspect
from dataclasses import dataclass
from typing import Callable, Any, Self


class ClosedForEditException(Exception):
    pass


class NotRegisteredException(Exception):
    pass


@dataclass
class Item:
    key: object
    value: object
    arguments: dict[str, Any]


class Provide:

    _items = None

    def __class_getitem__(cls, key) -> object | Callable:
        try:
            if key not in cls._items:
                raise NotRegisteredException

            item = cls._items[key]
            value = item.value
            kwargs = item.arguments

            if type(value) is not Callable:
                if len(
                        (params := inspect.signature(value).parameters)
                ) > 0:
                    for params_key, params_value in params.items():
                        if (param_to_resolve := params_value.annotation) in cls._items:
                            resolved = cls.__class_getitem__(param_to_resolve)
                            kwargs[params_key] = resolved
                return value(**kwargs)
            else:
                return value
        except (AttributeError, NotRegisteredException) as e:
            return None


class Container:
    def __init__(self) -> None:
        self.is_closed = False
        self._items = {}

    def register(self, key: object, value: object | Callable, **kwargs) -> None:
        if self.is_closed:
            raise ClosedForEditException

        self._items[key] = Item(key, value, kwargs)

    def wire(self) -> Self:
        Provide._items = self._items
        return self

    def close_edit(self):
        self.is_closed = True
