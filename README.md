# static_analysis
# Lab 5: Static Code Analysis Report

This document outlines the issues identified and fixed in the `inventory_system.py` file, along with reflections on the static analysis process.

---

## Deliverable 2: Issue Documentation Table

The following table documents the most critical issues found by Pylint, Bandit, and Flake8, their descriptions, and the approach taken to fix them. At least four issues were fixed, with a focus on high/medium severity findings.

| Issue Type (Tool) | Line(s) (Original) | Description | Fix Approach |
| :--- | :--- | :--- | :--- |
| **Security (Bandit)** | `60` | `B307: eval` - The `eval()` function was used, which is a significant security risk that can lead to arbitrary code execution. | **Removed the line.** The function `eval("print('eval used')")` served no functional purpose and was replaced with a simple, safe `print()` statement. |
| **Bug (Pylint)** | `8` | `W0102: dangerous-default-value` - The `addItem` function used `logs=[]` (a mutable list) as a default argument. This list is shared across all calls, leading to buggy, cumulative logging. | **Refactored to use `logging`.** The buggy `logs` parameter was removed. The imported `logging` module was properly configured in `main()` and used for clean, standard logging. |
| **Bug (Pylint)** | `16-18` | `W0702: broad-except` - The `removeItem` function used a bare `except:` clause. This is dangerous as it catches *all* errors (including `SystemExit`), making the program hard to debug. | **Used specific exception.** The `except:` was replaced with `except KeyError:`. This now correctly catches only the expected error (when an item is not in the dictionary). |
| **Bug/Style (Pylint)** | `24, 29` | **Unsafe file handling** - `loadData` and `saveData` used `f = open()` without a `with` statement. If an error occurred, `f.close()` would never be called, leaking file handles. | **Implemented `with open(...) as f:`.** This construct guarantees that the file is automatically closed, even if errors occur. `encoding="utf-8"` was also added. |
| **Bug (Logical)** | `21` | **`KeyError` risk** - `getQty` directly accessed `stock_data[item]`. If called with an item that doesn't exist, the program would crash with a `KeyError`. | **Used `.get()` method.** The code was changed to `return stock_data.get(item, 0)`. This safely returns the item's value or a default (0) if it does not exist. |
| **Bug (Pylint)** | `32` | **`W0603: Using the global statement`** - `loadData` used the `global` keyword to re-assign `stock_data`. This is generally bad practice. | **Refactored to mutate the global.** Instead of `global stock_data`, the function now mutates the dictionary in-place using `stock_data.clear()` and `stock_data.update()`. |
| **Style (Flake8)** | `1-62` | **PEP 8 Violations** - Flake8 flagged numerous issues: `camelCase` function names (e.g., `addItem`), missing docstrings, and improper spacing. | **Applied PEP 8 standards.** Renamed all functions to `snake_case` (e.g., `add_item`), added module and function docstrings, and fixed whitespace. |
| **Style (Pylint)** | `30, 37, etc.` | **`W1203: logging-fstring-interpolation`** - Pylint warned against using f-strings for logging as they are less efficient ("lazy formatting"). | **Used old-style `%` formatting.** All `logging.error(f"...")` calls were converted to `logging.error("...", var)` for lazy evaluation. |

---
