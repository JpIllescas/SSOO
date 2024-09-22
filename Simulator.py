from collections import deque
from Event import Event
from EventQueue import EventQueue
from Scheduler import Scheduler
import matplotlib.pyplot as plt
import psutil
import time

class Simulator:
    def __init__(self, processes, algorithms, time_quantum=2):
        self.processes = processes
        self.algorithms = algorithms
        self.time_quantum = time_quantum
        self.event_queue = EventQueue()
        self.blocked_queue = []
        self.metrics = {algo: {'turnaround': [], 'waiting': [], 'response': [], 'throughput': [], 'cpu_utilization': []} for algo in algorithms}
        self.total_time = 0

    def run(self, selected_algorithm):
        print(f"\nSimulando algoritmo: {selected_algorithm}")
        scheduler = Scheduler(selected_algorithm, self.time_quantum)
        current_time = 0
        metrics = {'turnaround': [], 'waiting': [], 'response': [], 'cpu_time': 0}
        process_count = len(self.processes)
        cpu_idle_time = 0

        for process in self.processes:
            process.remaining_time = process.burst_time
            process.state = 'listo'
            process.start_time = None
            process.finish_time = None
            process.response_time = None
            arrival_event = Event(process.arrival_time, 'arrival', process)
            self.event_queue.add_event(arrival_event)

        while not self.event_queue.is_empty() or scheduler.has_processes() or self.blocked_queue:
            event = self.event_queue.get_next_event() if not self.event_queue.is_empty() else None

            self.check_blocked_processes()

            if event and (scheduler.has_processes() == False or event.time <= current_time):
                current_time = event.time
                if event.event_type == 'arrival':
                    scheduler.add_process(event.process)
                    print(f"Proceso {event.process.id} llegó en el tiempo {event.time}")
                    time.sleep(1)  # Pausa para simular la llegada del proceso
            else:
                process = scheduler.get_next_process()
                if process:
                    if process.start_time is None:
                        process.start_time = current_time
                        process.response_time = current_time - process.arrival_time
                        metrics['response'].append(process.response_time)

                    if not self.check_resources(process):
                        process.state = 'bloqueado'
                        self.blocked_queue.append(process)
                        print(f"Proceso {process.id} bloqueado por falta de recursos")
                        continue

                    exec_time = self.time_quantum if selected_algorithm == 'Round Robin' else process.burst_time
                    exec_time = min(exec_time, process.remaining_time)
                    print(f"Ejecutando proceso {process.id} por {exec_time} unidades de tiempo...")
                    time.sleep(exec_time)  # Pausa para simular la ejecución del proceso
                    current_time += exec_time
                    metrics['cpu_time'] += exec_time
                    process.remaining_time -= exec_time

                    if process.remaining_time == 0:
                        process.finish_time = current_time
                        process.state = 'terminado'
                        turnaround = process.finish_time - process.arrival_time
                        waiting = turnaround - process.burst_time
                        metrics['turnaround'].append(turnaround)
                        metrics['waiting'].append(waiting)
                        print(f"Proceso {process.id} ha terminado en el tiempo {current_time}")
                    elif process.remaining_time > 0:
                        # Solo reinsertar si tiene tiempo restante y es Round Robin
                        if selected_algorithm == 'Round Robin':
                            scheduler.add_process(process)
                            print(f"Proceso {process.id} ejecutado por {exec_time} unidades de tiempo; tiempo restante {process.remaining_time}")
                        else:
                            # Evitar reinsertar para algoritmos que no son Round Robin
                            print(f"Proceso {process.id} tiene tiempo restante, pero no se reinserta en {selected_algorithm}")

        self.total_time = current_time
        throughput = process_count / self.total_time
        cpu_utilization = metrics['cpu_time'] / self.total_time * 100

        self.metrics[selected_algorithm]['turnaround'].extend(metrics['turnaround'])
        self.metrics[selected_algorithm]['waiting'].extend(metrics['waiting'])
        self.metrics[selected_algorithm]['response'].extend(metrics['response'])
        self.metrics[selected_algorithm]['throughput'].append(throughput)
        self.metrics[selected_algorithm]['cpu_utilization'].append(cpu_utilization)

    def check_blocked_processes(self):
        # Revisar procesos bloqueados y tratar de desbloquearlos
        for process in self.blocked_queue[:]:
            if self.check_resources(process):
                process.state = 'listo'
                self.blocked_queue.remove(process)
                print(f"Proceso {process.id} ha sido desbloqueado y movido a 'listo'")

    def check_resources(self, process):
        # Simulación basada en recursos reales (CPU y memoria)
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Establecemos umbrales de recursos
        cpu_threshold = 80  # Bloquear si el uso de CPU está por encima del 80%
        memory_threshold = 90  # Bloquear si la memoria está por encima del 90%

        if cpu_usage > cpu_threshold or memory_info.percent > memory_threshold:
            print(f"Proceso {process.id} bloqueado: Uso de CPU = {cpu_usage}%, Memoria = {memory_info.percent}%")
            return False  # Se bloquea el proceso si los recursos están por encima de los umbrales

        return True  # No se bloquea si hay suficientes recursos
                
    def visualize(self):
        algorithms = self.algorithms
        avg_turnaround = [sum(self.metrics[algo]['turnaround']) / len(self.metrics[algo]['turnaround']) if self.metrics[algo]['turnaround'] else 0 for algo in algorithms]
        avg_waiting = [sum(self.metrics[algo]['waiting']) / len(self.metrics[algo]['waiting']) if self.metrics[algo]['waiting'] else 0 for algo in algorithms]
        avg_response = [sum(self.metrics[algo]['response']) / len(self.metrics[algo]['response']) if self.metrics[algo]['response'] else 0 for algo in algorithms]
        avg_throughput = [sum(self.metrics[algo]['throughput']) for algo in algorithms]
        avg_cpu_utilization = [sum(self.metrics[algo]['cpu_utilization']) for algo in algorithms]

        plt.figure(figsize=(18, 8))

        plt.subplot(2, 3, 1)
        plt.bar(algorithms, avg_turnaround, color='blue')
        plt.title('Promedio de Turnaround Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Turnaround Time Promedio')

        plt.subplot(2, 3, 2)
        plt.bar(algorithms, avg_waiting, color='green')
        plt.title('Promedio de Waiting Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Waiting Time Promedio')

        plt.subplot(2, 3, 3)
        plt.bar(algorithms, avg_response, color='purple')
        plt.title('Promedio de Response Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Response Time Promedio')

        plt.subplot(2, 3, 4)
        plt.bar(algorithms, avg_throughput, color='orange')
        plt.title('Throughput')
        plt.xlabel('Algoritmo')
        plt.ylabel('Procesos Completados/Unidad de Tiempo')

        plt.subplot(2, 3, 5)
        plt.bar(algorithms, avg_cpu_utilization, color='red')
        plt.title('CPU Utilization')
        plt.xlabel('Algoritmo')
        plt.ylabel('CPU Utilization (%)')

        plt.tight_layout()
        plt.show()