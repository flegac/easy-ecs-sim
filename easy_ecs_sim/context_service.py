from typing import Type

from easy_ecs_sim.context import Context


class ContextService:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def find[T](self, ctype: Type[T]):
        return self.ctx.find(ctype)
