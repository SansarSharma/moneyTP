# utils/input_validators.py

"""
Utility functions for validating user input values.

Abstraction Function:
- InputValidators provides reusable methods to check and clean numeric input.

Representation Invariant:
- All methods return safe Python types (float, bool, etc.) or raise ValueError on failure.
"""


class InputValidators:
    @staticmethod
    def is_valid_float(text):
        """
        Checks if the given string is a valid float.

        REQUIRES: text is a string
        MODIFIES: nothing
        EFFECTS: Returns True if text is a valid float, False otherwise.
        """
        try:
            float(text)
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_positive_float(text):
        """
        Converts string to float if positive.

        REQUIRES: text is a valid float string
        MODIFIES: nothing
        EFFECTS: Returns the float if it's >= 0, otherwise raises ValueError.
        """
        value = float(text)
        if value < 0:
            raise ValueError("Value must be non-negative")
        return value

    @staticmethod
    def safe_float(text, fallback=0.0):
        """
        Attempts to parse float or returns fallback.

        REQUIRES: text is a string
        MODIFIES: nothing
        EFFECTS: Returns float(text) or fallback if invalid.
        """
        try:
            return float(text)
        except (TypeError, ValueError):
            return fallback
