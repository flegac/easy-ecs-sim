from dataclasses import field, dataclass
from typing import Self

from easy_kit.timing import time_func

from easy_ecs_sim.component import Component
from easy_ecs_sim.utils import ComponentSet, flatten_components
from easy_ecs_sim.signature import Signature
from easy_ecs_sim.types import EntityId


@dataclass
class Demography:
    birth: list[list[Component]] = field(default_factory=list)
    death: set[EntityId] = field(default_factory=set)

    def clear(self):
        self.birth.clear()
        self.death.clear()

    def with_birth(self, items: list[ComponentSet]):
        self.birth.extend(map(flatten_components, items))
        return self

    def with_death(self, items: Component | Signature | list[Component | Signature]):
        if isinstance(items, Component | Signature):
            items = [items]
        self.death.update([_.eid for _ in items])
        return self

    @time_func
    def load(self, other: Self):
        if other is None:
            return self
        self.death.update(other.death)
        self.birth.extend(other.birth)
        return self
