from dataclasses import dataclass, field
from pprint import pprint

from easy_kit.timing import TimingTestCase

from easy_ecs_sim.utils import column_mapping


@dataclass
class Child:
    x: float
    xx: list[float] = field(default_factory=list)


@dataclass
class Parent:
    y: float
    child: Child
    children: list[Child] = field(default_factory=list)


class TestUtils(TimingTestCase):
    def test_it(self):
        xx = column_mapping(Parent)
        pprint(xx)
