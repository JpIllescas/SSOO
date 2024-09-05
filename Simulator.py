from collections import deque
from Event import Event
from EventQueue import EventQueue
from Scheduler import Scheduler
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, processes, algorithms, time_quantum=2):
        self.processes = processes
        self.algorithms = algorithms
        self.time_quantum = time_quantum
        self.event_queue = EventQueue()
        self.metrics = {algo: {'turnaround': [], 'waiting': [], 'response': []} for algo in algorithms}  # Añadir response time
        self.cpu_idle_time = 0  # Para rastrear el tiempo de inactividad de la CPU

    def run(self, selected_algorithm):
        print(f"\nSimulando algoritmo: {selected_algorithm}")
        scheduler = Scheduler(selected_algorithm, self.time_quantum)
        current_time = 0
        event_queue = EventQueue()
        metrics = {'turnaround': [], 'waiting': [], 'response': []}
        cpu_idle = 0

        # Reiniciar procesos
        for process in self.processes:
            process.remaining_time = process.burst_time
            process.state = 'ready'
            process.start_time = None
            process.finish_time = None
            process.response_time = None  # Inicializamos el tiempo de respuesta
            arrival_event = Event(process.arrival_time, 'arrival', process)
            event_queue.add_event(arrival_event)

        # Simulación
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
                        process.response_time = current_time - process.arrival_time  # Calculamos el tiempo de respuesta
                        metrics['response'].append(process.response_time)
                    exec_time = self.time_quantum if selected_algorithm == 'Round Robin' else process.burst_time
                    exec_time = min(exec_time, process.remaining_time)
                    current_time += exec_time
                    process.remaining_time -= exec_time
                    if process.remaining_time == 0:
                        process.finish_time = current_time
                        turnaround = process.finish_time - process.arrival_time
                        waiting = turnaround - process.burst_time
                        metrics['turnaround'].append(turnaround)
                        metrics['waiting'].append(waiting)
                        print(f"Proceso {process.id} completado en el tiempo {current_time}")
                    else:
                        scheduler.add_process(process)
                        print(f"Proceso {process.id} ejecutado por {exec_time} unidades de tiempo; tiempo restante {process.remaining_time}")
                else:
                    # CPU idle, no hay procesos listos
                    idle_time = event.time - current_time if event else 1
                    cpu_idle += idle_time
                    current_time += idle_time
                    print(f"CPU ociosa durante {idle_time} unidades de tiempo")

        # Calcular promedios
        avg_turnaround = sum(metrics['turnaround']) / len(metrics['turnaround']) if metrics['turnaround'] else 0
        avg_waiting = sum(metrics['waiting']) / len(metrics['waiting']) if metrics['waiting'] else 0
        avg_response = sum(metrics['response']) / len(metrics['response']) if metrics['response'] else 0
        self.metrics[selected_algorithm]['turnaround'].append(avg_turnaround)
        self.metrics[selected_algorithm]['waiting'].append(avg_waiting)
        self.metrics[selected_algorithm]['response'].append(avg_response)
        self.cpu_idle_time = cpu_idle
        print(f"Promedio Turnaround Time para {selected_algorithm}: {avg_turnaround}")
        print(f"Promedio Waiting Time para {selected_algorithm}: {avg_waiting}")
        print(f"Promedio Response Time para {selected_algorithm}: {avg_response}")
        print(f"Tiempo total de inactividad de la CPU: {cpu_idle}")

    def visualize(self):
        algorithms = self.algorithms
        avg_turnaround = [self.metrics[algo]['turnaround'][0] if self.metrics[algo]['turnaround'] else 0 for algo in algorithms]
        avg_waiting = [self.metrics[algo]['waiting'][0] if self.metrics[algo]['waiting'] else 0 for algo in algorithms]
        avg_response = [self.metrics[algo]['response'][0] if self.metrics[algo]['response'] else 0 for algo in algorithms]

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
