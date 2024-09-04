# simulator.py
from Event import Event
from EventQueue import EventQueue
from Scheduler import Scheduler
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, processes, algorithms, time_quantum=2):
        self.processes = processes
        self.algorithms = algorithms  # Lista de algoritmos a simular
        self.time_quantum = time_quantum
        self.event_queue = EventQueue()
        self.metrics = {algo: {'turnaround': [], 'waiting': []} for algo in algorithms}

    def run(self):
        for algo in self.algorithms:
            print(f"\nSimulando algoritmo: {algo}")
            scheduler = Scheduler(algo, self.time_quantum)
            current_time = 0
            event_queue = EventQueue()
            metrics = {'turnaround': [], 'waiting': []}

            # Reiniciar procesos
            for process in self.processes:
                process.remaining_time = process.burst_time
                process.state = 'ready'
                process.start_time = None
                process.finish_time = None
                # Agregar evento de llegada
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
                        exec_time = self.time_quantum if algo == 'Round Robin' else process.burst_time
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
                            scheduler.add_process(process)  # Re-añadir al final si no terminó
                            print(f"Proceso {process.id} ejecutado por {exec_time} unidades de tiempo; tiempo restante {process.remaining_time}")
            # Calcular promedios
            avg_turnaround = sum(metrics['turnaround']) / len(metrics['turnaround']) if metrics['turnaround'] else 0
            avg_waiting = sum(metrics['waiting']) / len(metrics['waiting']) if metrics['waiting'] else 0
            self.metrics[algo]['turnaround'].append(avg_turnaround)
            self.metrics[algo]['waiting'].append(avg_waiting)
            print(f"Promedio Turnaround Time para {algo}: {avg_turnaround}")
            print(f"Promedio Waiting Time para {algo}: {avg_waiting}")

    def visualize(self):
        algorithms = self.algorithms
        avg_turnaround = [self.metrics[algo]['turnaround'][0] for algo in algorithms]
        avg_waiting = [self.metrics[algo]['waiting'][0] for algo in algorithms]

        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.bar(algorithms, avg_turnaround, color='blue')
        plt.title('Promedio de Turnaround Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Turnaround Time Promedio')

        plt.subplot(1, 2, 2)
        plt.bar(algorithms, avg_waiting, color='green')
        plt.title('Promedio de Waiting Time')
        plt.xlabel('Algoritmo')
        plt.ylabel('Waiting Time Promedio')

        plt.tight_layout()
        plt.show()
