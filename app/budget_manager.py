# app/budget_manager.py

"""
A Singleton that manages the user's global budget and transaction history.

Abstraction Function:
- BudgetManager holds the central state of the app including budget, transactions, and file state.

Representation Invariant:
- budget is a valid Budget object
- transactions is a list of valid Transaction objects
"""

from models.budget import Budget
from models.transaction import Transaction

class BudgetManager:
    _instance = None

    def __new__(cls):
        """
        Ensures only one instance of BudgetManager exists.

        REQUIRES: nothing
        MODIFIES: BudgetManager._instance
        EFFECTS: Returns the singleton instance of BudgetManager.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.budget = Budget()
            cls._instance.transactions = []
        return cls._instance

    def set_budget(self, amount):
        """
        Sets the budget limit.

        REQUIRES: amount >= 0
        MODIFIES: self.budget
        EFFECTS: Updates the budget limit for the session.
        """
        self.budget = Budget(amount)

    def add_transaction(self, transaction):
        """
        Adds a transaction to the current session.

        REQUIRES: transaction is an instance of Transaction
        MODIFIES: self.transactions
        EFFECTS: Appends the transaction and updates total spent.
        """
        self.transactions.append(transaction)
        self._update_total_spent()

    def _update_total_spent(self):
        """
        Recalculates total spending.

        REQUIRES: nothing
        MODIFIES: self.budget
        EFFECTS: Sums all transactions and updates budget's total spent.
        """
        total = sum(t.amount for t in self.transactions)
        self.budget.update_spent(total)

    def reset(self):
        """
        Resets the manager to default state.

        REQUIRES: nothing
        MODIFIES: self
        EFFECTS: Clears all transactions and resets budget to 0.
        """
        self.budget = Budget()
        self.transactions = []
