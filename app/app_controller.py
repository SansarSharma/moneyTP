# app/app_controller.py

"""
Facade class that handles transitions between screens and session state.

Abstraction Function:
- AppController simplifies interactions between UI components and internal logic.

Representation Invariant:
- Only one AppController is active at a time per application session.
"""

from app.budget_manager import BudgetManager
from file_io.excel_loader import ExcelLoader

class AppController:
    def __init__(self, stacked_widget):
        """
        Initializes the app controller with UI screens.

        REQUIRES: stacked_widget is a QStackedWidget with welcome and main screens
        MODIFIES: self
        EFFECTS: Prepares controller to coordinate UI navigation.
        """
        self.stack = stacked_widget
        self.main_window = stacked_widget.main_window
        self.welcome_screen = stacked_widget.welcome_screen

    def upload_file(self, path):
        """
        Loads an Excel file and transitions to the main screen.

        REQUIRES: path is a valid .xlsx file path
        MODIFIES: BudgetManager, main_window
        EFFECTS: Loads budget data and updates main window UI.
        """
        data = ExcelLoader.load_budget_data(path)
        if data:
            BudgetManager().reset()  # Ensure clean state
            self.main_window.budget_data = data
            self.main_window.update_ui()
            self.stack.setCurrentWidget(self.main_window)

    def continue_without_file(self):
        """
        Proceeds to main screen with empty session.

        REQUIRES: nothing
        MODIFIES: stack
        EFFECTS: Loads main screen without preloaded file.
        """
        BudgetManager().reset()
        self.stack.setCurrentWidget(self.main_window)

    def save_and_exit(self):
        """
        Saves the session data to an Excel file and exits the app.

        REQUIRES: nothing
        MODIFIES: Excel file
        EFFECTS: Writes session data to file and closes the app.
        """
        ExcelLoader.save_budget_data(BudgetManager().transactions, self.main_window.budget_data)
