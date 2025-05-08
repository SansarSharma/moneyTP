# ui/welcome_screen.py

"""
Welcome screen offering entry points into the app.

Abstraction Function:
- WelcomeScreen lets the user upload a budget file, continue without one, or download the Excel template.

Representation Invariant:
- parent is a QStackedWidget
"""

import os
import shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

class WelcomeScreen(QWidget):
    def __init__(self, parent):
        """
        Constructs the welcome screen.

        REQUIRES: parent is QStackedWidget
        MODIFIES: self
        EFFECTS: Builds welcome UI with three button options.
        """
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Money Manager - Welcome")

        layout = QVBoxLayout()

        # App title
        self.title = QLabel("Money Manager", self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title)

        # Upload Excel file
        self.upload_button = QPushButton("Upload Excel File")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Continue without file
        self.continue_button = QPushButton("Continue Without File")
        self.continue_button.clicked.connect(self.continue_without_file)
        layout.addWidget(self.continue_button)

        # Download template
        self.download_button = QPushButton("Download Template")
        self.download_button.clicked.connect(self.download_template)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def upload_file(self):
        """
        Loads user-selected Excel file and transitions to main screen.

        REQUIRES: user selects valid Excel file
        MODIFIES: self.parent.main_window
        EFFECTS: Loads file into app and switches screen.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.parent.main_window.budget_data = self.parent.main_window.budget_data = self.parent.main_window.budget_data = self.parent.main_window.budget_data = self.parent.main_window.budget_data
            self.parent.main_window.load_budget_data(file_path)
            self.parent.setCurrentWidget(self.parent.main_window)

    def continue_without_file(self):
        """
        Goes straight to main screen with no data.

        REQUIRES: nothing
        MODIFIES: view
        EFFECTS: Switches to empty budget interface.
        """
        self.parent.setCurrentWidget(self.parent.main_window)

    def download_template(self):
        """
        Saves a copy of the default Excel template to user system.

        REQUIRES: template/templateFile.xlsx exists
        MODIFIES: file system
        EFFECTS: Opens file dialog and writes template to user-defined location.
        """
        source = os.path.join(os.getcwd(), "template", "templateFile.xlsx")

        if not os.path.exists(source):
            print("Template file not found!")
            return

        destination, _ = QFileDialog.getSaveFileName(self, "Save Template As", "", "Excel Files (*.xlsx)")
        if destination:
            shutil.copy(source, destination)
            print(f"Template saved to {destination}")
