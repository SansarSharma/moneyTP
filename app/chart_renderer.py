# app/chart_renderer.py

"""
Defines interchangeable strategies for rendering charts.

Abstraction Function:
- Each ChartRenderer defines a specific way to visualize spending data.
- The strategy can be changed at runtime to switch visual styles.

Representation Invariant:
- Each renderer implements a render(ax, data) method
"""

from abc import ABC, abstractmethod

class ChartRenderer(ABC):
    @abstractmethod
    def render(self, ax, data):
        """
        Renders a chart using the given axes and data.

        REQUIRES: ax is a matplotlib AxesSubplot; data is a list of numbers
        MODIFIES: ax
        EFFECTS: Plots the data using a specific chart style.
        """
        pass


class LineChartRenderer(ChartRenderer):
    def render(self, ax, data):
        """
        Renders data as a pointed line graph.

        REQUIRES: ax is a matplotlib AxesSubplot; data is a list of 7 numbers
        MODIFIES: ax
        EFFECTS: Displays the trend of expenses over a week with a line chart.
        """
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ax.plot(days, data, marker="o", linestyle="-", color="red", linewidth=2)
        ax.set_title("Spending Trends")
        ax.set_xlabel("Days of the Week")
        ax.set_ylabel("Cost ($)")
        ax.grid(True)
