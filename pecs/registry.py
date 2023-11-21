"""This module contains the Registry class."""

from collections import defaultdict
import uuid
import inspect


class Registry:
    """
    A registry stores and manages entities (or identifiers) and components.
    """

    def __init__(self):
        self.__entities = defaultdict(list)

    @staticmethod
    def __object_as_name(obj) -> str:
        """
        Get the concrete object name as a string.

        :param obj: Object
        :return: string
        """

        if inspect.isclass(obj):
            return obj.__name__
        elif isinstance(obj, object):
            return type(obj).__name__

    def create(self) -> int:
        """
        Constructs a naked entity with no components and returns its identifier.

        :return: identifier
        """

        # The first 64 bits of uuid1 is safer to use since there's no chance of a
        # collision. This is largely based on the clock, so there's much less randomness
        # but the uniqueness is better.
        identifier: int = uuid.uuid1().int >> 64
        self.__entities[identifier] = []
        return identifier

    def destroy(self, entity):
        """
        Destroys an entity and all its components.

        :param entity: Identifier
        :return: nothing
        """

        # Delete entity if it exists
        if entity in self.__entities:
            self.__entities.pop(entity, None)

    def valid(self, entity) -> bool:
        """
        Returns true if the entity is still valid, false otherwise.

        :param entity: Identifier
        :return: boolean
        """
        return entity in self.__entities

    def emplace(self, entity, component):
        """
        Creates, initializes and assigns to an entity the given component.

        :param entity: Identifier
        :param component: Component class or instance
        :return: component
        """

        duplicate = self.get(entity, component)
        if not duplicate:
            if inspect.isclass(component):
                self.__entities[entity].append(component())
            elif isinstance(component, object):
                self.__entities[entity].append(component)

            return self.__entities[entity][-1]

    def insert(self, component):
        """
        Assign the same component to all entities at once.

        :param component: Component class or instance
        :return: nothing
        """

        for key in self.__entities:
            self.emplace(key, component)

    def replace(self, entity, component):
        """
        Constructs a new instance and replaces the component.

        :param entity: Identifier
        :param component: Component class or instance.
        :return: component
        """

        duplicate = self.get(entity, component)
        if duplicate:
            if inspect.isclass(component):
                duplicate = component()
            elif isinstance(component, object):
                duplicate = component
            return duplicate

    def emplace_or_replace(self, entity, component):
        """
        When it's unknown whether an entity already owns an instance of a component, use
        this function instead.

        :param entity: Identifier
        :param component: Component class or instance
        :return: component
        """

        if self.all_of(entity, component):
            return self.replace(entity, component)
        else:
            return self.emplace(entity, component)

    def all_of(self, entity, *components: type) -> bool:
        """
        Verify that entity contains all the component types.

        :param entity: Identifier
        :param components: List of components
        :return: boolean
        """

        for i in components:
            if not self.get(entity, i):
                return False

        return True

    def any_of(self, entity, *components: type) -> bool:
        """
        Verify that entity contains at least one of the component types.

        :param entity: Identifier
        :param components: List of components
        :return: boolean
        """

        for i in components:
            if self.get(entity, i):
                return True

        return False

    def none_of(self, entity, *components: type) -> bool:
        """
        Verify that entity does not contain any of the component types.

        :param entity: Identifier
        :param components: List of components
        :return: boolean
        """

        count = 0
        for i in components:
            if not self.get(entity, i):
                count += 1
        return count == len(components)

    def remove(self, entity, component: type):
        """
        Delete the component from entity if it exists.

        :param entity: Identifier
        :param component: Component class
        :return: nothing
        """

        match = self.get(entity, component)
        if match:
            self.__entities[entity].remove(match)

    def clear(self, *components: type):
        """
        If given no argument, it destroys all entities in the registry.
        If given a list of components, it erases those components from the entities.

        :param components: List of components
        :return: nothing
        """

        if components:
            # Erases all instances of the given components from the entities
            for component in components:
                for key in self.__entities:
                    self.remove(key, component)
        else:
            self.__entities.clear()  # Destroy all entities

    def get(self, entity, component):
        """
        Checks for component and if found, returns the component from the entity.

        :param entity: Identifier
        :param component: Component class
        :return: component
        """

        component_name: str = self.__object_as_name(component)
        for i in self.__entities[entity]:
            if type(i).__name__ == component_name:
                return i

    def view(self, *components: type) -> list:
        """
        Retrieve a list of entities that contains the given components.

        :param components: List of components
        :return: list
        """

        entities = []
        for component in components:
            for key in self.__entities:
                if self.get(key, component):
                    entities.append(key)
        return entities
