from typing import Type

from easy_ecs_sim.system import System, SystemBag


class Systems:
    def __init__(self, systems: list[System] = None):
        self.systems = systems or []

    def flatten(self):
        systems = []
        for _ in self.systems:
            if isinstance(_, SystemBag):
                systems.extend(_.steps)
            else:
                systems.append(_)
        return systems

    def find[T: System](self, stype: Type[T]):
        for sys in self.flatten():
            if isinstance(sys, stype):
                return sys

    def insert(self, index: int, item: System):
        self.systems.insert(index, item)

    def append(self, item: System):
        self.systems.append(item)
