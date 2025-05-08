# Main.py

"""
Launches the Money Manager application.

Abstraction Function:
- Main creates the QStackedWidget and manages transitions between WelcomeScreen and MainWindow.

Representation Invariant:
- App starts in full-screen mode.
- Screens are properly registered in the QStackedWidget.
"""

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from ui.welcome_screen import WelcomeScreen
from ui.main_window import MainWindow

def main():
    """
    Starts the PyQt6 application and shows the welcome screen.

    REQUIRES: Python 3.8+, PyQt6 installed
    MODIFIES: UI window
    EFFECTS: Displays the full-screen budget management app.
    """
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    # Screens
    welcome = WelcomeScreen(stacked_widget)
    main_window = MainWindow(stacked_widget)

    # Assign navigation access
    stacked_widget.welcome_screen = welcome
    stacked_widget.main_window = main_window

    # Register screens
    stacked_widget.addWidget(welcome)
    stacked_widget.addWidget(main_window)

    # Show welcome screen
    stacked_widget.setCurrentWidget(welcome)
    stacked_widget.showFullScreen()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
