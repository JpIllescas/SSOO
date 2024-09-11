# scheduler.py
from collections import deque
from process import Process

class Scheduler:
    def __init__(self, algorithm, time_quantum=2):
        self.algorithm = algorithm
        self.time_quantum = time_quantum
        self.ready_queue = deque()

    def add_process(self, process):
        self.ready_queue.append(process)

    def get_next_process(self):
        if self.algorithm == 'FIFO':
            return self.ready_queue.popleft() if self.ready_queue else None
        elif self.algorithm == 'SJF':
            if not self.ready_queue:
                return None
            # Selecciona el proceso con el burst_time más corto
            shortest = min(self.ready_queue, key=lambda p: p.burst_time)
            self.ready_queue.remove(shortest)
            return shortest
        elif self.algorithm == 'Round Robin':
            if self.ready_queue:
                process = self.ready_queue.popleft()
                if process.remaining_time > 0:
                    self.add_process(process)  # Solo usa una llamada para re-insertar
                return process
            return None
        elif self.algorithm == 'Prioridad':
            if not self.ready_queue:
                return None
            # Selecciona el proceso con la prioridad más alta
            highest_priority = max(self.ready_queue, key=lambda p: p.priority)
            self.ready_queue.remove(highest_priority)
            return highest_priority
        else:
            raise ValueError(f'Algoritmo desconocido: {self.algorithm}')

    def has_processes(self):
        return len(self.ready_queue) > 0
