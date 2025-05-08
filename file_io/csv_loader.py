# file_io/csv_loader.py

"""
Adapter that allows CSV budget files to be loaded in the same format as Excel files.

Abstraction Function:
- CsvLoader converts CSV-format budgets into a dictionary identical to what ExcelLoader returns.

Representation Invariant:
- Returned dictionary has keys: "Income", "Balance", "Expenses".
"""

import csv
from file_io.file_parser_interface import FileParserInterface


class CsvLoader(FileParserInterface):
    def load_budget_data(self, path):
        """
        Loads CSV file and adapts it to the same structure used by ExcelLoader.

        REQUIRES: path is a valid CSV file path
        MODIFIES: nothing
        EFFECTS: Returns parsed budget data as dictionary.
        """
        data = {
            "Income": {
                "Projected Monthly Income": 0.0,
                "Actual Monthly Income": 0.0
            },
            "Balance": {
                "Projected Balance": 0.0,
                "Actual Balance": 0.0,
                "Difference": 0.0
            },
            "Expenses": {}
        }

        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row["Category"].strip().upper()
                item = row["Item"].strip()
                projected = float(row["Projected Cost"])
                actual = float(row["Actual Cost"])

                if category not in data["Expenses"]:
                    data["Expenses"][category] = []

                data["Expenses"][category].append({
                    "Item": item,
                    "Projected Cost": projected,
                    "Actual Cost": actual
                })

        # Dummy balance calc (since CSV might not include summary)
        all_projected = sum(item["Projected Cost"] for cat in data["Expenses"].values() for item in cat)
        all_actual = sum(item["Actual Cost"] for cat in data["Expenses"].values() for item in cat)

        data["Income"]["Projected Monthly Income"] = all_projected + 500  # Placeholder logic
        data["Income"]["Actual Monthly Income"] = all_actual + 500
        data["Balance"]["Projected Balance"] = 500.0
        data["Balance"]["Actual Balance"] = 500.0
        data["Balance"]["Difference"] = 0.0

        return data
