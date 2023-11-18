import pecs

from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float


def update(registry: pecs.Registry):
    view: list = registry.view(Position)
    for entity in view:
        pos = registry.get(entity, Position)
        ...


def main():
    registry = pecs.Registry()

    for i in range(10):
        entity = registry.create()
        registry.emplace(entity, Position(i * 2, i))

    update(registry)


if __name__ == "__main__":
    main()
