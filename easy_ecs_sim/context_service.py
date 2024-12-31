from typing import Type, TypeVar

from easy_ecs_sim.context import Context

T = TypeVar('T')


class ContextService:

    @classmethod
    def singleton(cls: Type[T]) -> T:
        return cls(Context.default())

    def __init__(self, ctx: Context):
        self.ctx = ctx
        ctx.register(self)

    def find[T](self, ctype: Type[T]):
        return self.ctx.find(ctype)
