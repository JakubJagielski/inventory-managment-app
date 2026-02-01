import pytest
from django.urls import reverse
from atmio.inventory.models import Component


@pytest.mark.django_db
def test_component_table_identifier_filter(client, fake_component_1, fake_component_2, fake_component_3):
    """
    Given I have multiple components in the database
    When I request the components table
    And I provide a component identifier as a filter
    Then I should only see components matching that identifier
    """
    url = reverse("component_table")

    # Exact match
    response = client.get(url, {"filter_identifier": "FAKE_COMPONENT_1"})
    content = response.content.decode()
    assert "FAKE_COMPONENT_1" in content
    assert "FAKE_COMPONENT_2" not in content
    assert "FAKE_COMPONENT_§" not in content

    # Partial match
    """
    Given I have multiple components in the database
    When I request the components table
    And I provide a partial identifier as a filter
    Then I should see all components containing that identifier
    """
    response = client.get(url, {"filter_identifier": "FAKE_COMPONENT"})
    content = response.content.decode()
    for c in ["FAKE_COMPONENT_1", "FAKE_COMPONENT_2", "FAKE_COMPONENT_3"]:
        assert c in content

@pytest.mark.django_db
def test_component_table_inventory_level_filter(client, fake_component_1, fake_component_2, fake_component_3, fake_inventory_level_1, fake_inventory_level_2):
    """
    Given I have components assigned to multiple inventory levels
    When I filter by inventory level 1
    Then I should see only components belonging to inventory level 1
    """
    url = reverse("component_table")

    response = client.get(url, {"filter_inventory_level": fake_inventory_level_1.id})
    content = response.content.decode()
    assert "FAKE_COMPONENT_1" in content
    assert "FAKE_COMPONENT_2" in content
    assert "FAKE_COMPONENT_3" not in content

    """
    Given I have components assigned to multiple inventory levels
    When I filter by inventory level 2
    Then I should see only components belonging to inventory level 2
    """
    response = client.get(url, {"filter_inventory_level": fake_inventory_level_2.id})
    content = response.content.decode()
    assert "FAKE_COMPONENT_3" in content
    assert "FAKE_COMPONENT_1" not in content
    assert "FAKE_COMPONENT_2" not in content


@pytest.mark.django_db
def test_component_table_sorting(client, fake_component_1, fake_component_2, fake_component_3):
    """
    Given I have multiple components
    When I sort by identifier ascending
    Then the components should appear in ascending identifier order
    """
    url = reverse("component_table")
    response = client.get(url, {"sort": "identifier", "dir": "asc"})
    content = response.content.decode()
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    idx3 = content.find("FAKE_COMPONENT_3")
    assert idx1 < idx2 < idx3

    """
    Given I have multiple components
    When I sort by identifier descending
    Then the components should appear in descending identifier order
    """
    response = client.get(url, {"sort": "identifier", "dir": "desc"})
    content = response.content.decode()
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    idx3 = content.find("FAKE_COMPONENT_3")
    assert idx3 < idx2 < idx1


@pytest.mark.django_db
def test_component_table_combined_filters(client, fake_component_1, fake_component_2, fake_component_3, fake_inventory_level_1):
    """
    Given I have multiple components across different inventory levels
    When I filter by inventory level 1 and identifier containing '2'
    Then only components that match both criteria should appear
    """
    url = reverse("component_table")
    response = client.get(url, {
        "filter_inventory_level": fake_inventory_level_1.id,
        "filter_identifier": "2"
    })
    content = response.content.decode()

    assert "FAKE_COMPONENT_2" in content
    assert "FAKE_COMPONENT_1" not in content
    assert "FAKE_COMPONENT_3" not in content


@pytest.mark.django_db
def test_component_table_sorting(client, fake_component_1, fake_component_2, fake_component_3):
    """
    Given I have multiple components
    When I sort by identifier ascending
    Then the components should appear in ascending identifier order
    """
    url = reverse("component_table")
    response = client.get(url, {"sort": "identifier", "dir": "asc", "filter_identifier": "FAKE_COMPONENT"})
    content = response.content.decode()
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    idx3 = content.find("FAKE_COMPONENT_3")
    assert idx1 < idx2 < idx3

    """
    Given I have multiple components
    When I sort by identifier descending
    Then the components should appear in descending identifier order
    """
    response = client.get(url, {"sort": "identifier", "dir": "desc", "filter_identifier": "FAKE_COMPONENT"})
    content = response.content.decode()
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    idx3 = content.find("FAKE_COMPONENT_3")
    assert idx3 < idx2 < idx1


@pytest.mark.django_db
def test_component_table_filter_and_sort(client, fake_component_1, fake_component_2, fake_component_3, fake_inventory_level_1):
    """
    Given I have multiple components in the database
    When I filter by inventory level 1
    And I sort by identifier ascending
    Then only components from inventory level 1 should appear
    And they should be sorted by identifier ascending
    """
    url = reverse("component_table")

    response = client.get(url, {
        "filter_identifier": "FAKE_COMPONENT",
        "filter_inventory_level": fake_inventory_level_1.id,
        "sort": "identifier",
        "dir": "asc"
    })
    content = response.content.decode()

    # Only components from inventory_level_1
    assert "FAKE_COMPONENT_1" in content
    assert "FAKE_COMPONENT_2" in content
    assert "FAKE_COMPONENT_3" not in content

    # Check ascending order
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    assert idx1 < idx2

    """
    Given I have multiple components in the database
    When I filter by inventory level 1
    And I sort by identifier descending
    Then only components from inventory level 1 should appear
    And they should be sorted by identifier descending
    """
    response = client.get(url, {
        "filter_identifier": "FAKE_COMPONENT",
        "filter_inventory_level": fake_inventory_level_1.id,
        "sort": "identifier",
        "dir": "desc"
    })
    content = response.content.decode()

    # Only components from inventory_level_1
    assert "FAKE_COMPONENT_1" in content
    assert "FAKE_COMPONENT_2" in content
    assert "FAKE_COMPONENT_3" not in content

    # Check descending order
    idx1 = content.find("FAKE_COMPONENT_1")
    idx2 = content.find("FAKE_COMPONENT_2")
    assert idx2 < idx1

import pytest
from django.urls import reverse
from django.db import IntegrityError
from atmio.inventory.models import Component, InventoryLevel


@pytest.mark.django_db
def test_component_create_success(client, fake_inventory_level_1):
    """
    Given I have an inventory level in the database
    When I post a new component with a unique identifier
    Then the component should be created
    And the HX-Trigger header should be set to 'inventoryUpdated'
    """
    url = reverse("component_create")
    data = {
        "identifier": "FAKE_COMPONENT_NEW",
        "description": "A new test component",
        "inventory_level": fake_inventory_level_1.id,
    }

    response = client.post(url, data)
    content = response.content.decode()

    # Component should exist
    comp = Component.objects.get(identifier="FAKE_COMPONENT_NEW")
    assert comp.description == "A new test component"
    assert comp.inventory_level == fake_inventory_level_1

    # HX-Trigger header should be present
    assert response["HX-Trigger"] == "inventoryUpdated"


@pytest.mark.django_db(transaction=True)
def test_component_create_duplicate_identifier_view(client, fake_component_1, fake_inventory_level_1):
    """
    Given I have a component with identifier 'FAKE_COMPONENT_1'
    When I POST a new component with the same identifier to the create endpoint
    Then the response should contain an error message
    And the component count should not increase
    """
    url = reverse("component_create")
    data = {
        "identifier": "FAKE_COMPONENT_1",
        "description": "Attempted duplicate",
        "inventory_level": fake_inventory_level_1.id,
    }

    response = client.post(url, data)
    content = response.content.decode()

    # Check that error message is displayed
    assert "A component with this identifier already exists." in content

    # Component count remains 1
    assert Component.objects.filter(identifier="FAKE_COMPONENT_1").count() == 1
