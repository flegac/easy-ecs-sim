from typing import Type, TypeVar

from easy_ecs_sim.context import Context

T = TypeVar('T')


class ContextService:

    @classmethod
    def default(cls: Type[T]) -> T:
        ctx = Context.default()
        if cls in ctx:
            return ctx.find(cls)
        return cls(ctx)

    def __init__(self, ctx: Context):
        self.ctx = ctx
        ctx.register(self)

    def find[T](self, ctype: Type[T]):
        return self.ctx.find(ctype)
