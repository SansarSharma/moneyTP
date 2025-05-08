# ui/widget_factory.py

"""
Provides a factory method to build preformatted table widgets for categories.

Abstraction Function:
- WidgetFactory creates reusable QTableWidgets to display budget data by category.

Representation Invariant:
- Tables must have 3 columns: Item, Projected Cost, Actual Cost
"""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class WidgetFactory:
    @staticmethod
    def create_budget_table(items):
        """
        Creates a new table widget from the given item data.

        REQUIRES: items is a list of dictionaries with keys 'Item', 'Projected Cost', 'Actual Cost'
        MODIFIES: nothing
        EFFECTS: Returns a QTableWidget filled with provided item data.
        """
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Item", "Projected Cost", "Actual Cost"])
        table.setRowCount(len(items))

        for row, item in enumerate(items):
            table.setItem(row, 0, QTableWidgetItem(item.get("Item", "")))
            table.setItem(row, 1, QTableWidgetItem(f"${item.get('Projected Cost', 0):.2f}"))
            table.setItem(row, 2, QTableWidgetItem(f"${item.get('Actual Cost', 0):.2f}"))

        return table
