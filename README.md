# Introduction
**pecs** is a library for integrating Entity Component System (ECS) with game
development. It is inspired by [**entt**](https://github.com/skypjack/entt),
another ECS library but for C++.

From [Wikipedia](https://en.wikipedia.org/wiki/Entity_component_system):

> **Entity component system (ECS)** is a software architectural pattern mostly
> used in video game development for the representation of game world objects.
> An ECS comprises _entities_ composed of _components_ of data, with _systems_
> which operate on entities' components.

## Code Example
```python
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
```

## Authors

Rakin Rahman

## License

This project is licensed under the MIT License - see the LICENSE file for details