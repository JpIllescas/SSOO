# process.py
class Process:
    def __init__(self, id, arrival_time, burst_time, priority=0):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.state = 'nuevo'
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.blocked = False

    def __repr__(self):
        return f'Process(id={self.id}, arrival_time={self.arrival_time}, burst_time={self.burst_time}, priority={self.priority}, state={self.state})'

    def set_state(self, new_state):
        self.state = new_state
