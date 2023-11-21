import pytest
import pecs


@pytest.fixture
def registry():
    yield pecs.Registry()


@pytest.fixture
def entity(registry):
    yield registry.create()


class Component:
    pass


class TestRegistry:
    def test_create(self, entity):
        assert entity is not None

    def test_destroy(self, registry, entity):
        registry.destroy(entity)
        assert registry.valid(entity) is False

    def test_valid(self, registry, entity):
        assert registry.valid(entity) is True

    def test_emplace(self, registry, entity):
        component = Component()
        assert registry.emplace(entity, component) == component

    def test_insert(self, registry):
        entities = []
        for i in range(10):
            entities.append(registry.create())

        registry.insert(Component)
        for entity in entities:
            if not registry.get(entity, Component):
                assert False

    def test_replace(self, registry, entity):
        registry.emplace(entity, Component)
        assert registry.replace(entity, Component) is not None

    def test_emplace_or_replace(self, registry, entity):
        component = registry.emplace(entity, Component)
        assert registry.emplace_or_replace(entity, Component) != component

    def test_all_of(self, registry, entity):
        registry.emplace(entity, Component)
        assert registry.all_of(entity, Component) is True

    def test_any_of(self, registry, entity):
        registry.emplace(entity, Component)
        assert registry.any_of(entity, Component) is True

    def test_none_of(self, registry, entity):
        assert registry.none_of(entity, Component) is True

    def test_remove(self, registry, entity):
        registry.emplace(entity, Component)
        registry.remove(entity, Component)
        assert registry.get(entity, Component) is None

    def test_clear(self, registry, entity):
        registry.clear()
        assert registry.valid(entity) is False

    def test_get(self, registry, entity):
        registry.emplace(entity, Component)
        assert registry.get(entity, Component) is not None

    def test_view(self, registry):
        entities = []
        for i in range(10):
            entity = registry.create()
            registry.emplace(entity, Component)
            entities.append(entity)

        view: list = registry.view(Component)
        assert set(view) == set(entities)
