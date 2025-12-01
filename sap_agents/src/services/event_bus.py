import logging
from typing import Callable, Dict, List, Any

logger = logging.getLogger(__name__)

class EventBus:
    _instance = None
    _subscribers: Dict[str, List[Callable]] = {}
    _history: List[Dict[str, Any]] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Subscribed to {event_type}")

    def publish(self, event_type: str, payload: Dict[str, Any]):
        logger.info(f"Publishing {event_type}: {payload}")
        self._history.append({"event": event_type, "payload": payload})
        
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                try:
                    handler(payload)
                except Exception as e:
                    logger.error(f"Error handling {event_type}: {e}")

    def get_history(self):
        return self._history

    def clear_history(self):
        self._history = []

event_bus = EventBus()
