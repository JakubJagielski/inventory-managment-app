import pytest
from inventory_manager.models import Component, InventoryLevel
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def use_test_db():
    settings.DATABASES['default'] = settings.DATABASES['test']

@pytest.fixture
def fake_inventory_level_1(db):
    return InventoryLevel.objects.create(name="FAKE_INVENTORY_LEVEL_1")

@pytest.fixture
def fake_inventory_level_2(db):
    return InventoryLevel.objects.create(name="FAKE_INVENTORY_LEVEL_2")

@pytest.fixture
def fake_component_1(db, fake_inventory_level_1):
    return Component.objects.create(
        identifier="FAKE_COMPONENT_1",
        description="Sample component",
        inventory_level=fake_inventory_level_1
    )

@pytest.fixture
def fake_component_2(db, fake_inventory_level_1):
    return Component.objects.create(
        identifier="FAKE_COMPONENT_2",
        description="Sample component",
        inventory_level=fake_inventory_level_1
    )

@pytest.fixture
def fake_component_3(db, fake_inventory_level_2):
    return Component.objects.create(
        identifier="FAKE_COMPONENT_3",
        description="Sample component",
        inventory_level=fake_inventory_level_2
    )
