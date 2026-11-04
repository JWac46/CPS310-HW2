
"""CPS 310 - Homework 2: Inventory Manager"""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


def load_inventory(filename):
    """Load inventory records from a pipe-delimited text file."""
    inventory = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                name, category, quantity = line.split("|")
                inventory.append({
                    "name": name,
                    "category": category,
                    "quantity": int(quantity)
                })
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save inventory records to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|'
                f'{item["quantity"]}\n'
            )


def validate_new_item(inventory, name, category, quantity):
    """Validate information for a new inventory item."""
    name = name.strip()
    category = category.strip()

    if not name:
        return "Item name cannot be empty."
    if "|" in name:
        return "Item name may not contain the | character."
    if not category:
        return "Category cannot be empty."
    if "|" in category:
        return "Category may not contain the | character."
    if not quantity.isdigit():
        return "Quantity must be a nonnegative whole number."

    for item in inventory:
        if item["name"].lower() == name.lower():
            return "An item with that name already exists."

    return None


def add_item_to_inventory(inventory, name, category, quantity):
    """Validate and add an item to inventory."""
    error = validate_new_item(inventory, name, category, quantity)

    if error:
        return False, error

    inventory.append({
        "name": name.strip(),
        "category": category.strip(),
        "quantity": int(quantity)
    })

    return True, "Item added successfully."


def find_matching_items(inventory, search_term):
    """Return inventory items matching a search term."""
    if not search_term.strip():
        return []

    return [
        item for item in inventory
        if search_term.lower() in item["name"].lower()
    ]


def remove_item_by_number(inventory, item_number):
    """Remove an item using its numbered position."""
    if not isinstance(item_number, int) or isinstance(item_number, bool):
        return None

    if item_number < 1 or item_number > len(inventory):
        return None

    return inventory.pop(item_number - 1)


def update_item_quantity(inventory, item_number, new_quantity):
    """Update the quantity of an inventory item."""
    if not isinstance(item_number, int) or isinstance(item_number, bool):
        return False

    if item_number < 1 or item_number > len(inventory):
        return False

    if not str(new_quantity).isdigit():
        return False

    inventory[item_number - 1]["quantity"] = int(new_quantity)
    return True


def calculate_summary(inventory):
    """Calculate inventory summary information."""
    category_counts = {}

    for item in inventory:
        category = item["category"].lower()

        if category not in category_counts:
            category_counts[category] = {
                "name": item["category"],
                "count": 0
            }

        category_counts[category]["count"] += 1

    return {
        "unique_items": len(inventory),
        "total_quantity": sum(item["quantity"] for item in inventory),
        "low_stock_items": sum(
            1 for item in inventory
            if item["quantity"] < LOW_STOCK_THRESHOLD
        ),
        "category_counts": category_counts
    }


def display_menu():
    """Display the main menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


def view_inventory(inventory):
    """Display all inventory items."""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory:")
    for index, item in enumerate(inventory, start=1):
        print(
            f'{index}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )


def add_item(inventory):
    """Collect information and add an inventory item."""
    name = input("Enter the item name: ")
    category = input("Enter the category: ")
    quantity = input("Enter the quantity: ").strip()

    success, message = add_item_to_inventory(
        inventory, name, category, quantity
    )

    if success:
        save_inventory(inventory, INVENTORY_FILE)

    print(message)


def update_quantity(inventory):
    """Collect information and update an item's quantity."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)

    selection_text = input("Enter the item number to update: ").strip()

    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return

    selection = int(selection_text)

    if selection < 1 or selection > len(inventory):
        print("Item number is outside the available range.")
        return

    quantity_text = input("Enter the new quantity: ").strip()

    if not update_item_quantity(inventory, selection, quantity_text):
        print("Quantity must be a nonnegative whole number.")
        return

    save_inventory(inventory, INVENTORY_FILE)
    print(f'{inventory[selection - 1]["name"]} quantity updated.')


def remove_item(inventory):
    """Collect information and remove an inventory item."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)

    selection_text = input("Enter the item number to remove: ").strip()

    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return

    removed_item = remove_item_by_number(
        inventory, int(selection_text)
    )

    if removed_item is None:
        print("Item number is outside the available range.")
        return

    save_inventory(inventory, INVENTORY_FILE)
    print(f'Item removed: {removed_item["name"]}')


def search_inventory(inventory):
    """Collect a search term and display matching items."""
    search_term = input("Enter part or all of an item name: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = find_matching_items(inventory, search_term)

    if not matches:
        print("No inventory items matched your search.")
        return

    print("\nSearch Results:")
    for index, item in enumerate(matches, start=1):
        print(
            f'{index}. {item["name"]} | {item["category"]} | '
            f'Quantity: {item["quantity"]}'
        )


def display_summary(inventory):
    """Display calculated inventory summary information."""
    summary = calculate_summary(inventory)

    print("\nInventory Summary")
    print(f'Unique items: {summary["unique_items"]}')
    print(f'Total quantity: {summary["total_quantity"]}')
    print(f'Low-stock items: {summary["low_stock_items"]}')

    print("\nItems by category:")

    if not summary["category_counts"]:
        print("No categories found.")
        return

    for category in summary["category_counts"].values():
        print(f'{category["name"]}: {category["count"]}')


def main():
    """Run the Inventory Manager menu loop."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
        elif choice == "3":
            update_quantity(inventory)
        elif choice == "4":
            remove_item(inventory)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a menu option from 1 through 7.")


if __name__ == "__main__":
    main()
