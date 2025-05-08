# file_io/excel_loader.py

"""
Excel loader that adapts Excel file I/O to the application's expected format.

Abstraction Function:
- ExcelLoader reads from or writes to Excel files in the template format.
- It acts as an adapter between pandas and the app's data model.

Representation Invariant:
- Files are read only if they match the template format (e.g., income, balance, expenses).
"""

import pandas as pd

class ExcelLoader:
    @staticmethod
    def load_budget_data(file_path):
        """
        Loads structured budget data from an Excel file.

        REQUIRES: file_path is a valid path to an .xlsx file
        MODIFIES: nothing
        EFFECTS: Returns a dictionary with Income, Balance, and Expenses from the Excel file.
        """
        try:
            income_df = pd.read_excel(file_path, sheet_name="Income")
            balance_df = pd.read_excel(file_path, sheet_name="Balance")
            expenses = {}

            sheet_names = pd.ExcelFile(file_path).sheet_names
            for sheet in sheet_names:
                if sheet not in ["Income", "Balance"]:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    expenses[sheet.upper()] = df.to_dict(orient="records")

            return {
                "Income": income_df.iloc[0].to_dict(),
                "Balance": balance_df.iloc[0].to_dict(),
                "Expenses": expenses
            }
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return {}

    @staticmethod
    def save_budget_data(transactions, budget_data):
        """
        Saves budget and transaction data back to an Excel file.

        REQUIRES: transactions is a list of dictionaries; budget_data is a structured dict
        MODIFIES: Creates a new Excel file
        EFFECTS: Writes structured sheets for income, balance, and each expense category.
        """
        try:
            with pd.ExcelWriter("UserBudgetExport.xlsx", engine="openpyxl") as writer:
                pd.DataFrame([budget_data["Income"]]).to_excel(writer, sheet_name="Income", index=False)
                pd.DataFrame([budget_data["Balance"]]).to_excel(writer, sheet_name="Balance", index=False)

                for category, items in budget_data["Expenses"].items():
                    df = pd.DataFrame(items)
                    df.to_excel(writer, sheet_name=category.title(), index=False)
        except Exception as e:
            print(f"Error saving Excel file: {e}")
