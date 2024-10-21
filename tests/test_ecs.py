from typing import override

from easy_kit.context import Context
from easy_kit.timing import TimingTestCase
from pydantic import Field

from easy_ecs_sim.component import Component
from easy_ecs_sim.ecs import ECS
from easy_ecs_sim.signature import Signature
from easy_ecs_sim.storage.demography import Demography
from easy_ecs_sim.storage.id_generator import IdGenerator
from easy_ecs_sim.storage.my_database import MyDatabase
from easy_ecs_sim.system import System

GENERATOR = IdGenerator()


class Position(Component):
    x: int = 0
    y: int = 0


class Speed(Component):
    x: int = 0
    y: int = 0


class Info(Component):
    name: str = Field(default_factory=lambda: str(GENERATOR.new_id()))


class Move(Signature):
    pos: Position
    speed: Speed


class MoveSystem(System[Move]):
    _signature = Move

    @override
    def update_single(self, ctx: Context, db: MyDatabase, item: Move, dt: float):
        item.pos.x += item.speed.x
        item.pos.y += item.speed.y
        if item.pos.x > 3:
            return Demography().with_death(item.eid)
        if item.speed.y == 0:
            return Demography().with_birth([
                [Info()],
                [Info()],
                [Info(), Position(x=0, y=10), Speed(x=0, y=2)],
                [Info(), Position(x=100, y=100)],
            ])


class TestEcs(TimingTestCase):

    def test_ecs(self):
        # init systems
        ecs = ECS(systems=[
        ])

        # create some entities
        ecs.create_all([
            Info(),
            [Info(), Position(x=3)],
            [Info(), Speed(x=2, y=1)],
            [Position(y=2), Speed(y=2)],
            [Info(), Position(x=6, y=6), Speed(x=2, y=1)],
            [Info(), Position(x=2, y=2), Speed(x=0, y=0)],
        ])

        # run simulation
        print('* update')
        ecs.update()
        print('* update')
        ecs.update()

        # update systems
        ecs.systems.insert(0, MoveSystem())

        print('* update (move)')
        ecs.update()

        print('update (move)')
        ecs.update()
