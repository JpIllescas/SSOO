from collections import deque
from Event import Event
from EventQueue import EventQueue
from Scheduler import Scheduler
import matplotlib.pyplot as plt
import psutil

class Simulator:
    def __init__(self, processes, algorithms, time_quantum=2):
        self.processes = processes
        self.algorithms = algorithms
        self.time_quantum = time_quantum
        self.event_queue = EventQueue()
        self.metrics = {algo: {'turnaround': [], 'waiting': [], 'response': []} for algo in algorithms}
        self.cpu_idle_time = 0  # Para rastrear el tiempo de inactividad de la CPU

    def run(self, selected_algorithm):
        print(f"\nSimulando algoritmo: {selected_algorithm}")
        scheduler = Scheduler(selected_algorithm, self.time_quantum)
        current_time = 0
        event_queue = EventQueue()
        metrics = {'turnaround': [], 'waiting': [], 'response': []}
        cpu_idle = 0

        for process in self.processes:
            process.remaining_time = process.burst_time
            process.state = 'listo'
            process.start_time = None
            process.finish_time = None
            process.response_time = None
            arrival_event = Event(process.arrival_time, 'arrival', process)
            event_queue.add_event(arrival_event)

        while not event_queue.is_empty() or scheduler.has_processes():
            event = event_queue.get_next_event() if not event_queue.is_empty() else None
            if event and (scheduler.has_processes() == False or event.time <= current_time):
                current_time = event.time
                if event.event_type == 'arrival':
                    scheduler.add_process(event.process)
                    print(f"Proceso {event.process.id} llegó en el tiempo {event.time}")
            else:
                process = scheduler.get_next_process()
                if process:
                    if process.start_time is None:
                        process.start_time = current_time
                        process.response_time = current_time - process.arrival_time
                        metrics['response'].append(process.response_time)

                    # Definir `exec_time` aquí, según el algoritmo Round Robin o burst_time
                    exec_time = self.time_quantum if selected_algorithm == 'Round Robin' else process.burst_time
                    exec_time = min(exec_time, process.remaining_time)
                    current_time += exec_time
                    process.remaining_time -= exec_time

                    if process.remaining_time == 0:
                        process.finish_time = current_time
                        process.state = 'terminado'
                        turnaround = process.finish_time - process.arrival_time
                        waiting = turnaround - process.burst_time
                        metrics['turnaround'].append(turnaround)
                        metrics['waiting'].append(waiting)
                        print(f"Proceso {process.id} ha terminado en el tiempo {current_time}")
                    else:
                        scheduler.add_process(process)
                        print(f"Proceso {process.id} ejecutado por {exec_time} unidades de tiempo; tiempo restante {process.remaining_time}")

    # Método modificado para simular bloqueos basados en recursos reales
    def check_resources(self, process, rendimiento='medio'):
        # Obtener el uso de CPU y memoria
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()

        # Umbrales según el nivel de rendimiento
        if rendimiento == 'alto':
            cpu_threshold, memory_threshold = 90, 95
        elif rendimiento == 'bajo':
            cpu_threshold, memory_threshold = 70, 80
        else:  # rendimiento medio
            cpu_threshold, memory_threshold = 80, 90

        if cpu_usage > cpu_threshold or memory_info.percent > memory_threshold:
            print(f"Proceso {process.id} bloqueado: CPU {cpu_usage}%, Memoria {memory_info.percent}%")
            return False  # Proceso bloqueado
        return True  # Proceso tiene suficientes recursos

    def visualize(self):
        algorithms = self.algorithms
        avg_turnaround = [sum(self.metrics[algo]['turnaround']) / len(self.metrics[algo]['turnaround']) if self.metrics[algo]['turnaround'] else 0 for algo in algorithms]
        avg_waiting = [sum(self.metrics[algo]['waiting']) / len(self.metrics[algo]['waiting']) if self.metrics[algo]['waiting'] else 0 for algo in algorithms]
        avg_response = [sum(self.metrics[algo]['response']) / len(self.metrics[algo]['response']) if self.metrics[algo]['response'] else 0 for algo in algorithms]

        plt.figure(figsize=(18, 6))

        plt.subplot(1, 3, 1)
        plt.bar(algorithms, avg_turnaround, color='blue')
        plt.title('Promedio de Turnaround Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Turnaround Time Promedio')

        plt.subplot(1, 3, 2)
        plt.bar(algorithms, avg_waiting, color='green')
        plt.title('Promedio de Waiting Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Waiting Time Promedio')

        plt.subplot(1, 3, 3)
        plt.bar(algorithms, avg_response, color='purple')
        plt.title('Promedio de Response Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Response Time Promedio')

        plt.tight_layout()
        plt.show()
