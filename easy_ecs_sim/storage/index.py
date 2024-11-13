from dataclasses import field, dataclass
from typing import Type, Iterable, Any, Generator, TypeVar, Generic

from easy_ecs_sim.types import EntityId

T = TypeVar('T')


@dataclass
class Index(Generic[T]):
    ttype: Type[T]
    by_entity: dict[EntityId, T] = field(default_factory=dict)

    @property
    def entities(self):
        return set(self.by_entity.keys())

    def iter(self, eids: Iterable[EntityId] = None) -> Generator[T | None, Any, None]:
        if eids is None:
            yield from self.by_entity.values()
        else:
            for eid in eids:
                yield self.read(eid)

    @property
    def count(self):
        return len(self.by_entity)

    def create(self, item: T):
        self.by_entity[item.eid] = item

    def read(self, eid: EntityId):
        return self.by_entity.get(eid, None)

    def read_any(self):
        return next(iter(self.by_entity.values()))

    def destroy(self, eid: EntityId):
        return self.by_entity.pop(eid, None)

    def destroy_all(self, eids: Iterable[EntityId]):
        for _ in eids:
            self.destroy(_)

    def clear(self):
        self.by_entity.clear()
