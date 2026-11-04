import pytest

from inventory_manager import (
    load_inventory,
    save_inventory,
    validate_new_item,
    find_matching_items,
    remove_item_by_number,
    update_item_quantity,
    calculate_summary
)


# -------------------------------
# Reusable Fixture
# -------------------------------

@pytest.fixture
def sample_inventory():
    return [
        {"name": "Keyboard", "category": "Electronics", "quantity": 10},
        {"name": "Mouse", "category": "Electronics", "quantity": 4},
        {"name": "Notebook", "category": "School", "quantity": 5},
        {"name": "Pencil", "category": "School", "quantity": 2}
    ]


# -------------------------------
# 1. File Loading Tests
# -------------------------------

def test_load_inventory(tmp_path):
    # Arrange
    filename = tmp_path / "inventory.txt"
    filename.write_text(
        "Keyboard|Electronics|10\n\nMouse|Electronics|4\n",
        encoding="utf-8"
    )

    # Act
    inventory = load_inventory(filename)

    # Assert
    assert inventory == [
        {"name": "Keyboard", "category": "Electronics", "quantity": 10},
        {"name": "Mouse", "category": "Electronics", "quantity": 4}
    ]
    assert isinstance(inventory[0]["quantity"], int)


def test_load_missing_file(tmp_path):
    # Arrange
    filename = tmp_path / "missing.txt"

    # Act
    inventory = load_inventory(filename)

    # Assert
    assert inventory == []


# -------------------------------
# 2. File Saving Tests
# -------------------------------

def test_save_inventory(tmp_path, sample_inventory):
    # Arrange
    filename = tmp_path / "inventory.txt"

    # Act
    save_inventory(sample_inventory, filename)

    # Assert
    assert filename.read_text(encoding="utf-8") == (
        "Keyboard|Electronics|10\n"
        "Mouse|Electronics|4\n"
        "Notebook|School|5\n"
        "Pencil|School|2\n"
    )


def test_save_empty_and_round_trip(tmp_path, sample_inventory):
    # Arrange
    filename = tmp_path / "inventory.txt"

    # Act
    save_inventory([], filename)

    # Assert
    assert filename.read_text(encoding="utf-8") == ""

    # Act
    save_inventory(sample_inventory, filename)
    loaded_inventory = load_inventory(filename)

    # Assert
    assert loaded_inventory == sample_inventory


def test_load_ignores_blank_lines(tmp_path):
    # Arrange
    filename = tmp_path / "inventory.txt"
    filename.write_text(
        "Keyboard|Electronics|10\n\nMouse|Electronics|4\n",
        encoding="utf-8"
    )

    # Act
    inventory = load_inventory(filename)

    # Assert
    assert len(inventory) == 2


def test_save_empty_inventory(tmp_path):
    # Arrange
    filename = tmp_path / "inventory.txt"

    # Act
    save_inventory([], filename)

    # Assert
    assert filename.read_text(encoding="utf-8") == ""


