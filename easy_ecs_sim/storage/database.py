from abc import ABC, abstractmethod
from typing import Type, TypeVar

from easy_ecs_sim.component import Component
from easy_ecs_sim.signature import Signature
from easy_ecs_sim.storage.index import Index
from easy_ecs_sim.types import EntityId
from easy_ecs_sim.utils import ComponentSet

T = TypeVar('T')


class Database(ABC):

    @abstractmethod
    def entities(self) -> set[EntityId]:
        ...

    @abstractmethod
    def create_all(self, items: list[ComponentSet]):
        ...

    @abstractmethod
    def destroy_all(self, items: Component | Signature | list[Component | Signature]):
        ...

    @abstractmethod
    def get_table[T:Component | Signature](self, ttype: Type[T]) -> Index[T]:
        ...

    @abstractmethod
    def find_any[T: Component](self, what: Type[T], having: list[Type[Component]]) -> T:
        ...
