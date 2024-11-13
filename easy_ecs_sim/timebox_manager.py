import time
from dataclasses import dataclass, field
from typing import Type, TypeVar, Generic

from easy_ecs_sim.storage.database import Database

T = TypeVar('T')


@dataclass
class TimeboxManager(Generic[T]):
    signature: Type[T]
    max_time_per_step: float
    items: list[T] = field(default_factory=list)
    dt_bonus: float = 0

    def iter(self, db: Database, dt: float):
        if len(self.items) == 0:
            self.items = list(db.get_table(self.signature).iter())
            self.dt_bonus = 0

        start = time.time()
        while time.time() - start < self.max_time_per_step:
            if len(self.items) == 0:
                break
            yield self.items.pop()
        self.dt_bonus += dt
