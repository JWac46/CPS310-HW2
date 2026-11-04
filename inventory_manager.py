"""CPS 310 - Homework 1: Inventory Manager
Instructor solution checkpoint.
"""

INVENTORY_FILE = "inventory.txt"
LOW_STOCK_THRESHOLD = 5


def display_menu():
    """Display the main Inventory Manager menu."""
    print("\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")


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
                inventory.append(
                    {
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                    }
                )
    except FileNotFoundError:
        return []

    return inventory


def save_inventory(inventory, filename):
    """Save the complete inventory to a pipe-delimited text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for item in inventory:
            file.write(
                f'{item["name"]}|{item["category"]}|{item["quantity"]}\n'
            )


def view_inventory(inventory):
    """Display all inventory items in a numbered list."""
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
    """Prompt for and add one validated inventory item, then save it."""
    name = input("Enter the item name: ").strip()
    if not name:
        print("Item name cannot be empty.")
        return
    if "|" in name:
        print("Item name may not contain the | character.")
        return

    for item in inventory:
        if item["name"].lower() == name.lower():
            print("An item with that name already exists.")
            return

    category = input("Enter the category: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    if "|" in category:
        print("Category may not contain the | character.")
        return

    quantity_text = input("Enter the quantity: ").strip()
    if not quantity_text.isdigit():
        print("Quantity must be a nonnegative whole number.")
        return

    quantity = int(quantity_text)
    inventory.append({"name": name, "category": category, "quantity": quantity})
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added successfully.")


def update_quantity(inventory):
    """Prompt for an item number and replace its quantity, then save it."""
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
    if not quantity_text.isdigit():
        print("Quantity must be a nonnegative whole number.")
        return

    quantity = int(quantity_text)
    item = inventory[selection - 1]
    item["quantity"] = quantity
    save_inventory(inventory, INVENTORY_FILE)
    print(f'{item["name"]} quantity updated to {quantity}.')


def remove_item(inventory):
    """Prompt for an item number, remove that item, then save the inventory."""
    if not inventory:
        print("No inventory items found.")
        return

    view_inventory(inventory)
    selection_text = input("Enter the item number to remove: ").strip()
    if not selection_text.isdigit():
        print("Item number must be a valid whole number.")
        return

    selection = int(selection_text)
    if selection < 1 or selection > len(inventory):
        print("Item number is outside the available range.")
        return

    removed_item = inventory.pop(selection - 1)
    save_inventory(inventory, INVENTORY_FILE)
    print(f'Item removed: {removed_item["name"]}')


def search_inventory(inventory):
    """Prompt for an item-name search term and display matching items."""
    search_term = input("Enter part or all of an item name: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return

    matches = []
    for item in inventory:
        if search_term.lower() in item["name"].lower():
            matches.append(item)

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
    """Calculate and display inventory summary information."""
    unique_items = len(inventory)
    total_quantity = 0
    low_stock_items = 0
    category_counts = {}
    category_labels = {}

    for item in inventory:
        total_quantity += item["quantity"]

        if item["quantity"] < LOW_STOCK_THRESHOLD:
            low_stock_items += 1

        category_key = item["category"].lower()
        if category_key not in category_counts:
            category_counts[category_key] = 0
            category_labels[category_key] = item["category"]
        category_counts[category_key] += 1

    print("\nInventory Summary")
    print(f"Unique items: {unique_items}")
    print(f"Total quantity: {total_quantity}")
    print(f"Low-stock items: {low_stock_items}")
    print("\nItems by category:")

    if not category_counts:
        print("No categories found.")
        return

    for category_key, count in category_counts.items():
        print(f"{category_labels[category_key]}: {count}")


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
