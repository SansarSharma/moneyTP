# ui/main_window.py

"""
Main screen showing user budget, tables, and chart.

Abstraction Function:
- MainWindow shows budget categories, a chart, and user interactions like save & exit.

Representation Invariant:
- parent is a QStackedWidget
- chart_canvas is not None
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QHBoxLayout, QGroupBox, QGridLayout, QScrollArea
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from models.budget import Budget
from models.category import Category
from app.chart_renderer import LineChartRenderer
from file_io.excel_loader import ExcelLoader

class MainWindow(QWidget):
    def __init__(self, parent):
        """
        Constructs the main dashboard screen.

        REQUIRES: parent is QStackedWidget
        MODIFIES: self
        EFFECTS: Builds all input fields, category tables, chart, and action buttons.
        """
        super().__init__()
        self.parent = parent
        self.budget_data = {}
        self.budget = Budget()

        # Outer layout
        layout = QVBoxLayout()

        # Scroll Area for vertical flow
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        # Upload + Budget Input
        self.upload_button = QPushButton("Upload Excel File")
        self.upload_button.clicked.connect(self.upload_file)
        scroll_layout.addWidget(self.upload_button)

        budget_layout = QHBoxLayout()
        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText("Enter Budget Limit")
        self.set_budget_button = QPushButton("Set Budget")
        self.set_budget_button.clicked.connect(self.set_budget)
        budget_layout.addWidget(self.budget_input)
        budget_layout.addWidget(self.set_budget_button)
        scroll_layout.addLayout(budget_layout)

        self.income_label = QLabel("Income: Not Loaded")
        self.balance_label = QLabel("Balance: Not Loaded")
        scroll_layout.addWidget(self.income_label)
        scroll_layout.addWidget(self.balance_label)

        # Categories
        self.categories = Category.all()
        self.category_sections = {}

        grid = QGridLayout()
        row, col = 0, 0
        for category in self.categories:
            box = QGroupBox(category)
            box_layout = QVBoxLayout()
            table = QTableWidget()
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Item", "Projected Cost", "Actual Cost"])
            box_layout.addWidget(table)
            box.setLayout(box_layout)
            self.category_sections[category] = table
            grid.addWidget(box, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        scroll_layout.addLayout(grid)

        # Budget status
        self.budget_status = QLabel("Budget Status: Not Set")
        scroll_layout.addWidget(self.budget_status)

        # Chart
        self.chart_canvas = FigureCanvas(plt.Figure(figsize=(12, 5)))
        scroll_layout.addWidget(self.chart_canvas)

        # Buttons
        self.back_button = QPushButton("Back to Welcome Screen")
        self.back_button.clicked.connect(self.go_back)
        self.save_button = QPushButton("Save & Exit")
        self.save_button.clicked.connect(self.save_and_exit)
        scroll_layout.addWidget(self.back_button)
        scroll_layout.addWidget(self.save_button)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def upload_file(self):
        """
        Opens a file and loads budget data.

        REQUIRES: valid Excel file selected
        MODIFIES: self.budget_data
        EFFECTS: Loads file and updates the entire UI.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.budget_data = ExcelLoader.load_budget_data(file_path)
            self.update_ui()

    def set_budget(self):
        """
        Updates the budget using user input.

        REQUIRES: valid number typed into budget_input
        MODIFIES: self.budget
        EFFECTS: Updates current budget object.
        """
        try:
            amount = float(self.budget_input.text())
            self.budget = Budget(amount)
            self.budget_status.setText(f"Budget Set: ${amount:.2f}")
            self.budget_input.clear()
        except ValueError:
            self.budget_status.setText("Invalid input!")

    def update_ui(self):
        """
        Redraws UI based on current loaded budget data.

        REQUIRES: self.budget_data is valid
        MODIFIES: UI widgets
        EFFECTS: Displays balance, income, tables, and chart.
        """
        if not self.budget_data:
            return

        income = self.budget_data["Income"]
        balance = self.budget_data["Balance"]
        self.income_label.setText(
            f"Projected Income: ${income['Projected Monthly Income']} | "
            f"Actual Income: ${income['Actual Monthly Income']}"
        )
        self.balance_label.setText(
            f"Projected Balance: ${balance['Projected Balance']} | "
            f"Actual Balance: ${balance['Actual Balance']} | "
            f"Difference: ${balance['Difference']}"
        )

        self.update_tables()
        self.update_budget_status()
        self.update_chart()

    def update_tables(self):
        """
        Fills the category tables with expense data.

        REQUIRES: self.budget_data["Expenses"] exists
        MODIFIES: category QTableWidgets
        EFFECTS: Fills tables with data from Excel
        """
        for category, table in self.category_sections.items():
            if category in self.budget_data["Expenses"]:
                items = self.budget_data["Expenses"][category]
                table.setRowCount(len(items))
                for row, item in enumerate(items):
                    table.setItem(row, 0, QTableWidgetItem(item["Item"]))
                    table.setItem(row, 1, QTableWidgetItem(f"${item['Projected Cost']}"))
                    table.setItem(row, 2, QTableWidgetItem(f"${item['Actual Cost']}"))

    def update_budget_status(self):
        """
        Updates label with budget summary info.

        REQUIRES: self.budget and expenses exist
        MODIFIES: budget_status QLabel
        EFFECTS: Sets warning or remaining budget message.
        """
        total_spent = sum(
            sum(item["Actual Cost"] for item in category if item["Actual Cost"] is not None)
            for category in self.budget_data["Expenses"].values()
        )
        self.budget.update_spent(total_spent)

        if self.budget.is_over_budget():
            self.budget_status.setText(f"Warning: Over Budget! ${total_spent:.2f} spent.")
        else:
            self.budget_status.setText(f"Budget Remaining: ${self.budget.remaining_budget():.2f}")

    def update_chart(self):
        """
        Draws weekly spending trend chart.

        REQUIRES: budget_data["Expenses"] exists
        MODIFIES: self.chart_canvas
        EFFECTS: Displays a line graph of costs per day.
        """
        expenses = self.budget_data["Expenses"]
        cost_data = [sum(item["Actual Cost"] for item in category) for category in expenses.values()]
        cost_data = cost_data[:7] + [0] * (7 - len(cost_data))

        self.chart_canvas.figure.clear()
        ax = self.chart_canvas.figure.add_subplot(111)
        renderer = LineChartRenderer()
        renderer.render(ax, cost_data)
        self.chart_canvas.draw()

    def go_back(self):
        """
        Returns user to welcome screen.

        REQUIRES: parent has welcome_screen
        MODIFIES: screen stack
        EFFECTS: Navigates to welcome view.
        """
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def save_and_exit(self):
        """
        Saves data to file and exits the app.

        REQUIRES: valid budget data
        MODIFIES: file system
        EFFECTS: Creates Excel file and closes app.
        """
        ExcelLoader.save_budget_data([], self.budget_data)
        self.close()
