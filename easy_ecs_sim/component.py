from dataclasses import field
from typing import Self, Type, Any, TypeVar

from easy_kit.my_model import MyModel
from easy_kit.timing import time_func

from easy_ecs_sim.context import Context
from easy_ecs_sim.storage.id_generator import IdGenerator
from easy_ecs_sim.types import ComponentId, EntityId

CID_GEN = IdGenerator()

T = TypeVar('T')


class Component(MyModel):
    cid: ComponentId = field(default_factory=CID_GEN.new_id)
    eid: EntityId = -1

    db: Any = None
    ctx: Context | None = None

    @classmethod
    def signature(cls) -> list[Type[Self]]:
        return [cls]

    @classmethod
    @time_func
    def cast(cls, items: list[Self]):
        for item in items:
            if isinstance(item, cls):
                return item

    @property
    def type_id(self):
        return self.__class__

    @time_func
    def get[T:Component](self, ctype: Type[T]) -> T | None:
        return self.db.get_table(ctype).read(self.eid)
