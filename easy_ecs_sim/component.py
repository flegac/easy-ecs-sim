from dataclasses import dataclass
from typing import Self, Type, Any, TypeVar

from easy_ecs_sim.context import Context

T = TypeVar('T')


@dataclass(kw_only=True)
class Component:
    eid: int = -1
    db: Any = None
    ctx: Context | None = None

    @property
    def cid(self):
        return id(self)

    @classmethod
    def signature(cls) -> list[Type[Self]]:
        return [cls]

    @classmethod
    def cast(cls, items: list[Self]):
        for item in items:
            if isinstance(item, cls):
                return item

    @property
    def type_id(self):
        return self.__class__

    def get[T:Component](self, ctype: Type[T]) -> T | None:
        return self.db.get_table(ctype).read(self.eid)
