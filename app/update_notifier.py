# app/update_notifier.py

"""
Implements a simple observer system for UI updates based on budget changes.

Abstraction Function:
- UpdateNotifier broadcasts state changes to all registered observers.

Representation Invariant:
- All observers must implement an `update()` method
"""

class Observer:
    def update(self):
        """
        Called when the observable data has changed.

        REQUIRES: Implemented by subclass
        MODIFIES: nothing
        EFFECTS: Reacts to data change (e.g., UI refresh).
        """
        raise NotImplementedError("Observer subclasses must implement update()")


class UpdateNotifier:
    def __init__(self):
        """
        Initializes a notifier for managing multiple observers.

        REQUIRES: nothing
        MODIFIES: self
        EFFECTS: Creates an empty observer list.
        """
        self.observers = []

    def register(self, observer):
        """
        Registers a new observer.

        REQUIRES: observer is an instance of Observer
        MODIFIES: self.observers
        EFFECTS: Adds the observer to the notification list.
        """
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        """
        Removes an observer from the list.

        REQUIRES: observer is already registered
        MODIFIES: self.observers
        EFFECTS: Stops the observer from being notified.
        """
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_all(self):
        """
        Notifies all registered observers.

        REQUIRES: nothing
        MODIFIES: observers
        EFFECTS: Calls update() on all registered observers.
        """
        for observer in self.observers:
            observer.update()
