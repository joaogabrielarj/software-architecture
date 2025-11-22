"""
Event Bus Implementation - Publish/Subscribe Pattern
Handles event distribution across all event processors in the system.
"""

from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Event:
    """Represents an event in the system."""
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventBus:
    """
    Event Bus implementation using Publish/Subscribe pattern.
    Allows event processors to subscribe to specific event types
    and automatically receive notifications when those events are published.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[Event] = []
        logger.info("Event Bus initialized")

    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        Subscribe a callback function to a specific event type.

        Args:
            event_type: The type of event to subscribe to
            callback: Function to call when event is published
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        self._subscribers[event_type].append(callback)
        logger.info(f"Subscriber registered for event type: {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """
        Unsubscribe a callback from an event type.

        Args:
            event_type: The event type to unsubscribe from
            callback: The callback function to remove
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)
                logger.info(f"Subscriber removed from event type: {event_type}")
            except ValueError:
                logger.warning(f"Callback not found for event type: {event_type}")

    def publish(self, event_type: str, data: Dict[str, Any] = None) -> None:
        """
        Publish an event to all subscribed callbacks.

        Args:
            event_type: The type of event to publish
            data: Optional data associated with the event
        """
        event = Event(event_type=event_type, data=data or {})
        self._event_history.append(event)

        if event_type in self._subscribers:
            logger.debug(f"Publishing event: {event_type} to {len(self._subscribers[event_type])} subscribers")
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Error in subscriber callback for {event_type}: {e}")
        else:
            logger.debug(f"No subscribers for event type: {event_type}")

    def get_event_history(self) -> List[Event]:
        """Returns the history of all published events."""
        return self._event_history.copy()

    def clear_history(self) -> None:
        """Clears the event history."""
        self._event_history.clear()
        logger.info("Event history cleared")

    def get_subscribers_count(self, event_type: str = None) -> int:
        """
        Get the number of subscribers.

        Args:
            event_type: Optional event type to count subscribers for.
                       If None, returns total count across all event types.

        Returns:
            Number of subscribers
        """
        if event_type:
            return len(self._subscribers.get(event_type, []))
        return sum(len(callbacks) for callbacks in self._subscribers.values())
