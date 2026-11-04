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

# -------------------------------
# 3. Search Tests
# -------------------------------

def test_exact_search(sample_inventory):
    # Arrange
    search_term = "Keyboard"

    # Act
    results = find_matching_items(sample_inventory, search_term)

    # Assert
    assert len(results) == 1
    assert results[0]["name"] == "Keyboard"


def test_partial_case_insensitive_search(sample_inventory):
    # Arrange
    search_term = "key"

    # Act
    results = find_matching_items(sample_inventory, search_term)

    # Assert
    assert len(results) == 1
    assert results[0]["name"] == "Keyboard"


def test_search_no_matches_or_empty(sample_inventory):
    # Arrange
    no_match = "Monitor"
    empty_search = "   "

    # Act
    no_results = find_matching_items(sample_inventory, no_match)
    empty_results = find_matching_items(sample_inventory, empty_search)

    # Assert
    assert no_results == []
    assert empty_results == []


# -------------------------------
# 4. Remove Tests
# -------------------------------

@pytest.mark.parametrize(
    "item_number, expected_name, expected_length",
    [
        (1, "Keyboard", 3),
        (2, "Mouse", 3),
        (4, "Pencil", 3)
    ],
    ids=["remove-first", "remove-middle", "remove-last"]
)
def test_remove_item(sample_inventory, item_number, expected_name,
                     expected_length):
    # Arrange
    original_length = len(sample_inventory)

    # Act
    removed = remove_item_by_number(sample_inventory, item_number)

    # Assert
    assert removed["name"] == expected_name
    assert len(sample_inventory) == expected_length
    assert len(sample_inventory) == original_length - 1
    assert all(
        item["name"] != expected_name for item in sample_inventory
    )


def test_remove_invalid_numbers(sample_inventory):
    # Arrange
    original = [item.copy() for item in sample_inventory]

    # Act
    results = [
        remove_item_by_number(sample_inventory, number)
        for number in [0, -1, 5]
    ]

    # Assert
    assert results == [None, None, None]
    assert sample_inventory == original

# -------------------------------
# 5. Update Tests
# -------------------------------

def test_update_quantity(sample_inventory):
    # Arrange
    new_quantity = "20"

    # Act
    result = update_item_quantity(sample_inventory, 1, new_quantity)

    # Assert
    assert result is True
    assert sample_inventory[0]["quantity"] == 20
    assert sample_inventory[1]["quantity"] == 4


def test_update_quantity_to_zero(sample_inventory):
    # Arrange
    new_quantity = "0"

    # Act
    result = update_item_quantity(sample_inventory, 1, new_quantity)

    # Assert
    assert result is True
    assert sample_inventory[0]["quantity"] == 0


def test_update_invalid_values(sample_inventory):
    # Arrange
    original = [item.copy() for item in sample_inventory]

    # Act
    invalid_item = update_item_quantity(sample_inventory, 0, "10")
    too_large_item = update_item_quantity(sample_inventory, 5, "10")
    negative_quantity = update_item_quantity(sample_inventory, 1, "-5")

    # Assert
    assert invalid_item is False
    assert too_large_item is False
    assert negative_quantity is False
    assert sample_inventory == original


# -------------------------------
# 6. Add Validation Tests
# -------------------------------

def test_valid_new_item(sample_inventory):
    # Arrange
    name = "Monitor"
    category = "Electronics"
    quantity = "8"

    # Act
    result = validate_new_item(sample_inventory, name, category, quantity)

    # Assert
    assert result is None


@pytest.mark.parametrize(
    "name, category, quantity",
    [
        ("", "Electronics", "5"),
        ("Monitor", "", "5"),
        ("Mon|itor", "Electronics", "5"),
        ("Monitor", "Elec|tronics", "5"),
        ("Monitor", "Electronics", "-5"),
        ("Monitor", "Electronics", "abc"),
    ],
    ids=[
        "empty-name",
        "empty-category",
        "pipe-in-name",
        "pipe-in-category",
        "negative-quantity",
        "nonnumeric-quantity"
    ]
)
def test_invalid_new_item(sample_inventory, name, category, quantity):
    # Arrange
    original_length = len(sample_inventory)

    # Act
    result = validate_new_item(sample_inventory, name, category, quantity)

    # Assert
    assert result is not None
    assert len(sample_inventory) == original_length


def test_duplicate_item_names(sample_inventory):
    # Arrange
    existing_name = "Keyboard"
    different_capitalization = "KEYBOARD"

    # Act
    result1 = validate_new_item(
        sample_inventory, existing_name, "Electronics", "5"
    )
    result2 = validate_new_item(
        sample_inventory, different_capitalization, "Electronics", "5"
    )

    # Assert
    assert result1 is not None
    assert result2 is not None

