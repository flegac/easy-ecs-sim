import time
import traceback
from easy_kit.timing import time_func, timing

from easy_ecs_sim.component import Component
from easy_ecs_sim.context import Context
from easy_ecs_sim.storage.database import Database
from easy_ecs_sim.storage.demography import Demography
from easy_ecs_sim.storage.my_database import MyDatabase
from easy_ecs_sim.system import System
from easy_ecs_sim.systems import Systems
from easy_ecs_sim.types import EntityId
from easy_ecs_sim.utils import ComponentSet


class ECS:
    def __init__(self, ctx: Context = None):
        self.ctx: Context = ctx or Context()
        self.db = MyDatabase()
        self.systems = Systems()
        self.last_updates = {}
        self.is_running: bool = True

    def add_systems(self, *systems: System):
        for sys in systems:
            self.systems.append(sys)
        return self.connect(self.ctx)

    def connect(self, ctx: Context):
        self.ctx = ctx
        self.ctx.register(self)
        self.ctx.register(self.db, Database)
        for _ in self.systems.flatten():
            self.ctx.register(_)
        return self

    def set_running(self, status: bool = None):
        if status is None:
            status = not self.is_running
        self.is_running = status
        if self.is_running:
            self.last_updates = {}
        return self

    def create_all(self, items: list[ComponentSet]):
        self.db.create_all(items)
        return self

    @time_func
    def update(self):
        self.apply_demography()

        if not self.is_running:
            return

        now = time.time()
        for sys in self.systems.paused:
            self.last_updates[sys.__class__] = now

        for sys in self.systems.actives():
            sys_key = sys.__class__
            if sys_key not in self.last_updates:
                self.last_updates[sys_key] = now
            elapsed = now - self.last_updates[sys_key]
            if elapsed < sys.periodicity_sec:
                continue
            self.last_updates[sys_key] = now

            try:
                with timing(f'ECS.update.{sys.sys_id}'):
                    sys.update(self.ctx, self.db, elapsed)
            except Exception as e:
                print(f'{sys.sys_id}: {e}\n{traceback.format_exc()}')

    @time_func
    def apply_demography(self):
        status = Demography().load(self.db.dirty)
        self.db.dirty.clear()

        systems = [_ for _ in self.systems.flatten() if _._signature is not None]
        for sys in systems:
            for _ in status.death:
                self._handle_death(sys, _)
        for sys in systems:
            for _ in status.birth:
                self._handle_birth(sys, _)

        self.db.update_demography(status)

    def _handle_birth(self, sys: System, items: Component | list[Component]):
        if isinstance(items, Component):
            items = [items]
        for item in items:
            item.db = self.db
            item.ctx = self.ctx
        signature = sys._signature
        item = signature.cast(items)
        if item is not None:
            self.db.get_table(signature).create(item)
            sys.register(self.ctx, item)

    def _handle_death(self, sys: System, eid: EntityId):
        index = self.db.get_table(sys._signature)
        item = index.read(eid)
        if item:
            sys.unregister(self.ctx, item)
        index.destroy(eid)


# default simulator
sim = ECS()
