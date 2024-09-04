from collections import deque
from process import Process

class ProcessQueue:
    def __init__(self):
        self.queue = deque()
        self.current_time = 0

    def add_process(self, process):
        self.queue.append(process)

    def remove_process(self):
        if len(self.queue) > 0:
            return self.queue.popleft()
        else:
            return None

    def calculate_metrics(self, process):
        # Turnaround time: finish time - arrival time
        turnaround_time = process.finish_time - process.arrival_time
        # Waiting time: turnaround time - burst time
        waiting_time = turnaround_time - process.burst_time
        print(f"Process {process.id}: Turnaround Time = {turnaround_time}, Waiting Time = {waiting_time}")
        return turnaround_time, waiting_time

    def execute_fifo(self):
        print("\nEjecutando FIFO:")
        total_turnaround = 0
        total_waiting = 0
        count = 0
        while self.queue:
            process = self.remove_process()
            if process.start_time is None:
                process.start_time = self.current_time
            print(f'Executing Process {process.id} with burst time {process.burst_time}')
            self.current_time += process.burst_time
            process.finish_time = self.current_time
            process.state = "finished"
            print(f'Process {process.id} finished execution.')
            turnaround, waiting = self.calculate_metrics(process)
            total_turnaround += turnaround
            total_waiting += waiting
            count += 1
        if count > 0:
            avg_turnaround = total_turnaround / count
            avg_waiting = total_waiting / count
            print(f'FIFO: Average Turnaround Time = {avg_turnaround:.2f}')
            print(f'FIFO: Average Waiting Time = {avg_waiting:.2f}')

    def execute_sjf(self):
        print("\nEjecutando SJF:")
        self.queue = deque(sorted(self.queue, key=lambda p: p.burst_time))
        total_turnaround = 0
        total_waiting = 0
        count = 0
        while self.queue:
            process = self.remove_process()
            if process.start_time is None:
                process.start_time = self.current_time
            print(f'Executing Process {process.id} with burst time {process.burst_time}')
            self.current_time += process.burst_time
            process.finish_time = self.current_time
            process.state = "finished"
            print(f'Process {process.id} finished execution.')
            turnaround, waiting = self.calculate_metrics(process)
            total_turnaround += turnaround
            total_waiting += waiting
            count += 1
        if count > 0:
            avg_turnaround = total_turnaround / count
            avg_waiting = total_waiting / count
            print(f'SJF: Average Turnaround Time = {avg_turnaround:.2f}')
            print(f'SJF: Average Waiting Time = {avg_waiting:.2f}')

    def execute_rr(self, time_quantum):
        print("\nEjecutando Round Robin:")
        total_turnaround = 0
        total_waiting = 0
        count = 0
        while self.queue:
            process = self.remove_process()
            if process.start_time is None:
                process.start_time = self.current_time
            if process.burst_time > time_quantum:
                print(f'Executing Process {process.id} for {time_quantum} time units.')
                process.burst_time -= time_quantum
                self.current_time += time_quantum
                self.add_process(process)
            else:
                print(f'Executing Process {process.id} for {process.burst_time} time units.')
                self.current_time += process.burst_time
                process.finish_time = self.current_time
                print(f'Process {process.id} finished execution.')
                turnaround, waiting = self.calculate_metrics(process)
                total_turnaround += turnaround
                total_waiting += waiting
                count += 1
        if count > 0:
            avg_turnaround = total_turnaround / count
            avg_waiting = total_waiting / count
            print(f'Round Robin: Average Turnaround Time = {avg_turnaround:.2f}')
            print(f'Round Robin: Average Waiting Time = {avg_waiting:.2f}')

    def execute_priority(self):
        print("\nEjecutando Prioridad:")
        self.queue = deque(sorted(self.queue, key=lambda p: p.priority, reverse=True))
        total_turnaround = 0
        total_waiting = 0
        count = 0
        while self.queue:
            process = self.remove_process()
            if process.start_time is None:
                process.start_time = self.current_time
            print(f'Executing Process {process.id} with priority {process.priority} and burst time {process.burst_time}')
            self.current_time += process.burst_time
            process.finish_time = self.current_time
            process.state = "finished"
            print(f'Process {process.id} finished execution.')
            turnaround, waiting = self.calculate_metrics(process)
            total_turnaround += turnaround
            total_waiting += waiting
            count += 1
        if count > 0:
            avg_turnaround = total_turnaround / count
            avg_waiting = total_waiting / count
            print(f'Prioridad: Average Turnaround Time = {avg_turnaround:.2f}')
            print(f'Prioridad: Average Waiting Time = {avg_waiting:.2f}')


if __name__ == "__main__":
    pq = ProcessQueue()

    # Añadir procesos para FIFO
    p1 = Process(id=1, arrival_time=0, burst_time=5)
    p2 = Process(id=2, arrival_time=1, burst_time=3)
    
    pq.add_process(p1)
    pq.add_process(p2)
    
    # Ejecución de FIFO
    pq.execute_fifo()

    # Añadir procesos para SJF
    p3 = Process(id=3, arrival_time=0, burst_time=4)
    p4 = Process(id=4, arrival_time=1, burst_time=2)

    pq.add_process(p3)
    pq.add_process(p4)
    
    # Ejecución de SJF
    pq.execute_sjf()

    # Añadir procesos para Round Robin
    p5 = Process(id=5, arrival_time=0, burst_time=6)
    p6 = Process(id=6, arrival_time=1, burst_time=4)

    pq.add_process(p5)
    pq.add_process(p6)
    
    # Ejecución de Round Robin con time quantum = 2
    pq.execute_rr(time_quantum=2)

    # Añadir procesos para Prioridad
    p7 = Process(id=7, arrival_time=0, burst_time=5, priority=2)
    p8 = Process(id=8, arrival_time=1, burst_time=3, priority=1)
    p9 = Process(id=9, arrival_time=2, burst_time=4, priority=3)

    pq.add_process(p7)
    pq.add_process(p8)
    pq.add_process(p9)

    # Ejecución de Prioridad
    pq.execute_priority()
