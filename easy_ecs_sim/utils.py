import builtins
import dataclasses
from typing import Type, TypeVar

from easy_ecs_sim.component import Component
from easy_ecs_sim.signature import Signature

ComponentSet = Component | list[Component] | Signature | None

T = TypeVar('T')


def flatten_components(item: ComponentSet):
    if isinstance(item, Component):
        return [item]
    if isinstance(item, Signature):
        return item.to_components()
    return item


def column_mapping[T: dataclasses.dataclass](ctype: Type[T], prefix: str = ''):
    if not prefix:
        prefix = f'{ctype.__name__}'
    res = {}

    for field in dataclasses.fields(ctype):
        subtype = field.type
        name = f'{prefix}.{field.name}'

        if dataclasses.is_dataclass(field.type):
            res.update(column_mapping(subtype, prefix=name))
        else:
            match field.type:
                case builtins.int:
                    res[name] = field.type
                case builtins.float:
                    res[name] = field.type
                case builtins.bool:
                    res[name] = field.type
                case _:
                    res[name] = field.type
    return res
