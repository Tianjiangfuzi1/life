from typing import Callable, Dict, List, Any, DefaultDict
from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subs: DefaultDict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, fn: Callable[[Any], None]):
        self._subs[topic].append(fn)

    def publish(self, topic: str, payload: Any):
        for fn in self._subs.get(topic, []):
            try:
                fn(payload)
            except Exception as e:
                print(f"[eventbus] handler error for {topic}: {e}")
