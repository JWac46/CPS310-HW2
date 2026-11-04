# Inventory Manager Manual Testing Record

This file records the manual testing performed for the Homework 1 solution checkpoint. Homework 2 adds automated pytest tests; this manual record should remain in the repository for comparison.

| # | Feature | Input or Action | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|
| 1 | Missing file | Start when `inventory.txt` does not exist | Program begins with an empty inventory | Program began normally with an empty inventory | Pass |
| 2 | Empty inventory | View an empty inventory | `No inventory items found.` | Correct message displayed | Pass |
| 3 | Add item | Add `HDMI Cable`, `Electronics`, `6` | Item is added and saved | Item added and saved | Pass |
| 4 | Empty name | Enter only whitespace for item name | Item is rejected | Item was rejected | Pass |
| 5 | Duplicate name | Add `laptop charger` when `Laptop Charger` exists | Duplicate is rejected | Duplicate was rejected | Pass |
| 6 | Nonnumeric quantity | Enter `six` for quantity | Quantity is rejected | Quantity was rejected | Pass |
| 7 | Negative quantity | Enter `-2` for quantity | Quantity is rejected | Quantity was rejected | Pass |
| 8 | Update item | Update item 1 to quantity `12` | Correct item changes to 12 and is saved | Correct item updated and saved | Pass |
| 9 | Invalid item number | Enter an item number beyond the list length | Selection is rejected without crashing | Selection was rejected | Pass |
| 10 | Remove item | Remove an existing numbered item | Correct item is removed and saved | Correct item removed and saved | Pass |
| 11 | Partial search | Search for `charger` | Matching charger items are displayed | Matching items displayed | Pass |
| 12 | Case-insensitive search | Search using different capitalization | Matching item is still found | Matching item found | Pass |
| 13 | No search matches | Search for text not found in any name | No-match message is displayed | Correct message displayed | Pass |
| 14 | Inventory summary | View summary with known sample data | Unique count, total quantity, low-stock count, and category counts are correct | Summary values were correct | Pass |
| 15 | Persistence | Make a change, exit, and restart | Saved change remains after restart | Change remained after restart | Pass |
