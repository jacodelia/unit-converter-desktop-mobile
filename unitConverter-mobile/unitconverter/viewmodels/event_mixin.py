"""Pure-Python event system replacing PySide6 Signal/Slot.

Provides an EventMixin that ViewModels inherit from instead of QObject.
Works identically on desktop (PySide6) and mobile (Toga/Android).
"""

from collections import defaultdict
from typing import Any, Callable


class EventMixin:
    """Lightweight observable mixin providing emit/on/off for events.

    Usage in a ViewModel::

        class MyViewModel(EventMixin):
            def do_something(self):
                self.emit("value_changed", new_value)

    Usage in a View::

        vm.on("value_changed", self._handle_change)
    """

    def __init__(self) -> None:
        super().__init__()
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        """Register a listener for an event.

        Args:
            event: The event name (e.g. "category_changed").
            callback: The function to call when the event fires.
        """
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable[..., Any]) -> None:
        """Remove a listener for an event.

        Args:
            event: The event name.
            callback: The previously registered function.
        """
        try:
            self._listeners[event].remove(callback)
        except ValueError:
            pass

    def emit(self, event: str, *args: Any) -> None:
        """Fire an event, calling all registered listeners.

        Args:
            event: The event name.
            *args: Arguments passed to each listener.
        """
        for callback in self._listeners[event]:
            callback(*args)
