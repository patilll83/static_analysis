"""
inventory_system.py

A simple command-line inventory management system.
This module allows for adding, removing, and querying item quantities,
and supports loading/saving the inventory to a JSON file.
"""

import json
import logging
from typing import Dict, List

# Global variable for inventory stock
# Note: While globals are generally discouraged,
# we keep it for this lab's scope.
stock_data: Dict[str, int] = {}


# --- Core Functions ---

def add_item(item: str, qty: int):
    """
    Adds a specified quantity of an item to the inventory.

    Args:
        item (str): The name of the item to add.
        qty (int): The quantity to add. Must be a positive integer.
    """
    # Input validation
    if not isinstance(item, str) or item.strip() == "":
        logging.error(
            "[add_item] Invalid item name: %s. "
            "Must be a non-empty string.", item
        )
        return
    if not isinstance(qty, int) or qty < 0:
        logging.error(
            "[add_item] Invalid quantity: %s. "
            "Must be a non-negative integer.", qty
        )
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logging.info(
        "Added %s of '%s'. New total: %s", qty, item, stock_data[item]
    )


def remove_item(item: str, qty: int):
    """
    Removes a specified quantity of an item from the inventory.

    If the quantity to remove exceeds the stock, the item is removed entirely.

    Args:
        item (str): The name of the item to remove.
        qty (int): The quantity to remove. Must be a positive integer.
    """
    # Input validation
    if not isinstance(item, str) or item.strip() == "":
        logging.error("[remove_item] Invalid item name: %s.", item)
        return
    if not isinstance(qty, int) or qty < 0:
        logging.error(
            "[remove_item] Invalid quantity: %s. "
            "Must be a non-negative integer.", qty
        )
        return

    try:
        if qty >= stock_data[item]:
            del stock_data[item]
            logging.info("Removed all remaining stock of '%s'.", item)
        else:
            stock_data[item] -= qty
            logging.info(
                "Removed %s of '%s'. New total: %s",
                qty, item, stock_data[item]
            )
    except KeyError:
        # Specific exception catched, not a broad 'except:'
        logging.warning(
            "[remove_item] Attempted to remove non-existent item: '%s'",
            item
        )
    except TypeError:
        # Catch potential type issues if stock_data is corrupted
        logging.error(
            "[remove_item] Type error for item '%s'. Check data.", item
        )


def get_quantity(item: str) -> int:
    """
    Gets the current quantity of a specific item.

    Args:
        item (str): The name of the item to query.

    Returns:
        int: The quantity in stock. Returns 0 if item is not found.
    """
    # Use .get() for safe dictionary access, avoiding KeyError
    return stock_data.get(item, 0)


# --- Data Persistence ---

def load_data(file: str = "inventory.json"):
    """
    Loads inventory data from a JSON file into the global stock_data.

    Args:
        file (str, optional): The file to load from. Defaults to "inventory.json".
    """
    # We mutate the global dict, avoiding the 'global' keyword (W0603)
    try:
        # Use 'with open' for safe file handling (guarantees .close())
        # Added 'encoding="utf-8"' to prevent potential 'UnicodeDecodeError'
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
            if not data:
                logging.warning(
                    "File '%s' is empty. Initializing empty inventory.", file
                )
                stock_data.clear()
                return
            new_data = json.loads(data)
            stock_data.clear()  # Mutate existing dict
            stock_data.update(new_data)  # Mutate existing dict
            logging.info("Successfully loaded data from %s", file)
    except FileNotFoundError:
        logging.warning(
            "File '%s' not found. Starting with an empty inventory.", file
        )
        stock_data.clear()
    except json.JSONDecodeError:
        logging.error(
            "Could not decode JSON from '%s'. Starting with empty inventory.",
            file
        )
        stock_data.clear()
    except IOError as e:  # Catch specific IOErrors (W0718)
        logging.critical(
            "Failed to load data from '%s' due to an IO error: %s", file, e
        )
        stock_data.clear()


def save_data(file: str = "inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        file (str, optional): The file to save to. Defaults to "inventory.json".
    """
    try:
        # Use 'with open' and 'encoding="utf-8"'
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
        logging.info("Successfully saved data to %s", file)
    except IOError as e:  # Catch specific IOErrors (W0718)
        logging.error("Could not write to file '%s': %s", file, e)


# --- Reporting ---

def print_data():
    """Prints a formatted report of all items and their quantities."""
    print("\n--- Inventory Report ---")
    if not stock_data:
        print("No items in stock.")
    else:
        for item, quantity in stock_data.items():
            print(f"  {item}: {quantity}")
    print("------------------------\n")


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Gets a list of items with stock at or below a given threshold.

    Args:
        threshold (int, optional): The low-stock threshold. Defaults to 5.

    Returns:
        List[str]: A list of item names that are low in stock.
    """
    return [
        item for item, quantity in stock_data.items() if quantity <= threshold
    ]


# --- Main Execution ---

def main():
    """Main function to run the inventory system demonstration."""
    # Configure logging to show timestamp, level, and message
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.info("Starting inventory system...")
    load_data()  # Load existing data first

    add_item("apple", 10)
    add_item("banana", 20)

    # These invalid calls will now be caught and logged, not crash
    add_item("banana", -2)   # Invalid quantity
    add_item(123, 10)        # Invalid item name

    remove_item("apple", 3)
    remove_item("orange", 1)  # Will log a warning (non-existent)

    apple_stock = get_quantity("apple")
    print(f"Current apple stock: {apple_stock}")

    # This call is now safe and will return 0
    orange_stock = get_quantity("orange")
    print(f"Current orange stock: {orange_stock}")

    low_items = check_low_items()
    print(f"Low items (<= 5): {low_items}")

    save_data()

    # Security fix: Replaced dangerous 'eval'
    # eval("print('eval used')")
    print("Secure log: 'eval' function call was removed.")

    print_data()


# Standard Python practice: Use a main guard
# This allows the script to be imported without running main()
if __name__ == "__main__":
    main()