# event.py
class Event:
    def __init__(self, time, event_type, process):
        self.time = time
        self.event_type = event_type  # 'arrival' o 'completion'
        self.process = process

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f'Event(time={self.time}, type={self.event_type}, process={self.process.id})'
