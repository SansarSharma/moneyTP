# models/budget.py

"""
Represents the user's budget configuration and tracking for their expenses.

Abstraction Function:
- A Budget represents the user's budget limit and total money spent.
- It tracks the remaining amount and whether the user is over budget.

Representation Invariant:
- budget_limit >= 0
- total_spent >= 0
"""

class Budget:
    def __init__(self, budget_limit=0.0):
        """
        Constructs a new Budget with an optional limit.

        REQUIRES: budget_limit >= 0
        MODIFIES: self
        EFFECTS: Initializes the budget with a given limit and resets total spent.
        """
        self.budget_limit = max(0.0, budget_limit)
        self.total_spent = 0.0

    def update_spent(self, amount):
        """
        Updates the total amount spent in this budget.

        REQUIRES: amount >= 0
        MODIFIES: self
        EFFECTS: Sets the total spent value for the budget.
        """
        self.total_spent = max(0.0, amount)

    def remaining_budget(self):
        """
        Returns the remaining budget amount.

        REQUIRES: nothing
        MODIFIES: nothing
        EFFECTS: Returns budget_limit - total_spent, never negative.
        """
        return max(0.0, self.budget_limit - self.total_spent)

    def is_over_budget(self):
        """
        Checks if the budget has been exceeded.

        REQUIRES: nothing
        MODIFIES: nothing
        EFFECTS: Returns True if total_spent > budget_limit, otherwise False.
        """
        return self.total_spent > self.budget_limit
