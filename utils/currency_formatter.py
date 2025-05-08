# utils/currency_formatter.py

"""
Helper to format currency consistently throughout the app.

Abstraction Function:
- CurrencyFormatter ensures all currency values are displayed as strings like "$1,234.56".

Representation Invariant:
- format_dollar returns a properly formatted dollar string given a float.
"""


class CurrencyFormatter:
    @staticmethod
    def format_dollar(amount):
        """
        Formats a float as a dollar string (e.g., $1,234.56).

        REQUIRES: amount is a float or int
        MODIFIES: nothing
        EFFECTS: Returns a string representing the currency format.
        """
        return f"${amount:,.2f}"
