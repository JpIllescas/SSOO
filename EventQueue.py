# event_queue.py
import heapq

class EventQueue:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        heapq.heappush(self.events, (event.time, event))

    def get_next_event(self):
        if self.events:
            return heapq.heappop(self.events)[1]
        return None

    def is_empty(self):
        return len(self.events) == 0
