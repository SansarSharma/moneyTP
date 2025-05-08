# models/transaction.py

"""
Represents a single expense or financial transaction.

Abstraction Function:
- Each Transaction stores when the transaction occurred, what it was for,
  how much it cost, and a short description of the item/service.

Representation Invariant:
- date != None and is a string in format 'YYYY-MM-DD'
- category != None
- amount >= 0
"""

class Transaction:
    def __init__(self, date, category, amount, description=""):
        """
        Constructs a new Transaction with given attributes.

        REQUIRES: date and category are not None; amount >= 0
        MODIFIES: self
        EFFECTS: Initializes a transaction with date, category, amount, and optional description.
        """
        self.date = date
        self.category = category
        self.amount = max(0.0, amount)
        self.description = description

    def to_dict(self):
        """
        Returns the transaction details as a dictionary.

        REQUIRES: nothing
        MODIFIES: nothing
        EFFECTS: Converts the transaction into a dictionary format for serialization or display.
        """
        return {
            "Date": self.date,
            "Category": self.category,
            "Amount": self.amount,
            "Description": self.description
        }
