from dataclasses import dataclass


@dataclass
class IdGenerator:
    last_id: int = -1

    def new_id(self):
        self.last_id += 1
        return self.last_id

    def gen(self, n: int):
        return [self.new_id() for _ in range(n)]
