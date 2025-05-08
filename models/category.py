# models/category.py

"""
Defines reusable constants for expense categories.

Abstraction Function:
- Category stores all valid category names used across the app.

Representation Invariant:
- All categories are uppercase strings.
- No category name is empty or null.
"""


class Category:
    HOUSING = "HOUSING"
    TRANSPORTATION = "TRANSPORTATION"
    INSURANCE = "INSURANCE"
    SCHOOL = "SCHOOL"
    FOOD = "FOOD"
    PERSONAL_CARE = "PERSONAL CARE"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"
    HOLIDAY_EXPENSES = "HOLIDAY EXPENSES"
    MISCELLANEOUS = "MISCELLANEOUS"

    @staticmethod
    def all():
        """
        Returns all defined category constants as a list.

        REQUIRES: nothing
        MODIFIES: nothing
        EFFECTS: Provides access to all supported categories.

        :return: list of all category names.
        """
        return [
            Category.HOUSING,
            Category.TRANSPORTATION,
            Category.INSURANCE,
            Category.SCHOOL,
            Category.FOOD,
            Category.PERSONAL_CARE,
            Category.SUBSCRIPTIONS,
            Category.HOLIDAY_EXPENSES,
            Category.MISCELLANEOUS
        ]
