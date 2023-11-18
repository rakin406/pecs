import pytest
import pecs

# TODO: Fix the pytest ImportError.


@pytest.fixture
def registry():
    yield pecs.Registry()


class TestRegistry:
    def test_create(self, registry):
        assert registry.create() is not None

    def test_destroy(self, registry):
        entity = registry.create()
        registry.destroy(entity)
        assert registry.valid(entity) is False

    def test_valid(self):
        ...
        assert False

    def test_emplace(self):
        assert False

    def test_insert(self):
        assert False

    def test_replace(self):
        assert False

    def test_emplace_or_replace(self):
        assert False

    def test_all_of(self):
        assert False

    def test_any_of(self):
        assert False

    def test_remove(self):
        assert False

    def test_clear(self):
        assert False

    def test_get(self):
        assert False

    def test_view(self):
        assert False
