# file_io/parser_interface.py

"""
Interface for file parsers (Excel, CSV, etc.).

Abstraction Function:
- FileParserInterface provides a uniform API for any data loader used in the app.

Representation Invariant:
- Implementing classes must return a dict with keys: Income, Balance, Expenses.
"""

from abc import ABC, abstractmethod


class FileParserInterface(ABC):
    @abstractmethod
    def load_budget_data(self, path):
        """
        Loads budget data from file.

        REQUIRES: path is a valid file path
        MODIFIES: nothing
        EFFECTS: Returns a dictionary with keys: Income, Balance, Expenses.
        """
        pass
