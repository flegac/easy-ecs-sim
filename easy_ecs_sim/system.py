from abc import abstractmethod
from dataclasses import field
from typing import Type, override

from pydantic import model_validator

from easy_kit.my_model import MyModel
from easy_ecs_sim.component import Component
from easy_ecs_sim.signature import Signature
from easy_ecs_sim.storage.database import Database
from easy_ecs_sim.timebox_manager import TimeboxManager


class BaseSystem(MyModel):
    periodicity_sec: float = 0  # expected (or minimum) time between two updates

    def at_interval(self, periodicity_sec: float):
        self.periodicity_sec = periodicity_sec
        return self

    @abstractmethod
    def update(self, db: Database, dt: float):
        ...


class System[T: Signature | Component](BaseSystem):
    _signature: Type[T] = None
    max_time_per_step: float | None = None
    timebox: TimeboxManager[T] | None = None

    @model_validator(mode='after')
    def post_init(self):
        if self.max_time_per_step is not None:
            self.timebox = TimeboxManager(
                signature=self._signature,
                max_time_per_step=self.max_time_per_step
            )
        return self

    @property
    def sys_id(self):
        return self.__class__.__name__

    def update_single(self, db: Database, item: T, dt: float):
        pass

    def register(self, item: T):
        pass

    def unregister(self, item: T):
        pass

    @override
    def update(self, db: Database, dt: float):
        if self.timebox:
            dt_fixed = dt + self.timebox.dt_bonus
            for item in self.timebox.iter(db, dt):
                self.update_single(db, item, dt_fixed)
        else:
            for item in db.get_table(self._signature).iter():
                self.update_single(db, item, dt)


class SystemBag(System):
    name: str
    steps: list[System] = field(default_factory=list)

    def update(self, db: Database, dt: float):
        for _ in self.steps:
            _.update_all(db, dt)
