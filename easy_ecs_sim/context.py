from functools import lru_cache
from typing import Type, Any, TypeVar

T = TypeVar('T')


class Context:
    @classmethod
    @lru_cache(maxsize=None)
    def default(cls: Type[T]) -> T:
        return cls()

    def __init__(self, *initial_state: Any):
        self.data: dict[Type, Any] = {}
        for _ in initial_state:
            self.register(_)

    def find[T](self, ctype: Type[T]) -> T:
        return self.data[ctype]

    def register[T](self, data: T, ctype: Type[T] = None):
        found_type = type(data)

        if ctype is not None:
            if not issubclass(found_type, ctype):
                raise ValueError(f'incompatible type [{ctype}] for data of type [{found_type}]')

        if ctype is not None:
            assert issubclass(found_type, ctype)
        else:
            ctype = found_type
        self.data[ctype] = data
        return self

    def register_all(self, items: list):
        for _ in items:
            self.register(_)
        return self

    def clear(self):
        self.data.clear()
        return self
