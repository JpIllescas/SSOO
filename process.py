class Process:
    def __init__(self, id, arrival_time, burst_time, priority=0):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.state = 'ready'
        self.start_time = None  # Nuevo atributo para el tiempo de inicio
        self.finish_time = None  # Nuevo atributo para el tiempo de finalización

    def __repr__(self):
        return f'Process(id={self.id}, arrival_time={self.arrival_time}, burst_time={self.burst_time}, priority={self.priority}, state={self.state})'
