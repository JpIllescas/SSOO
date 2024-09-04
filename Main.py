# main.py
from process import Process
from Simulator import Simulator

def main():
    # Definir procesos
    procesos = [
        Process(id=1, arrival_time=0, burst_time=5),
        Process(id=2, arrival_time=1, burst_time=3),
        Process(id=3, arrival_time=0, burst_time=4),
        Process(id=4, arrival_time=1, burst_time=2),
        Process(id=5, arrival_time=0, burst_time=6),
        Process(id=6, arrival_time=1, burst_time=4),
        Process(id=7, arrival_time=0, burst_time=5, priority=2),
        Process(id=8, arrival_time=1, burst_time=3, priority=1),
        Process(id=9, arrival_time=2, burst_time=4, priority=3)
    ]

    # Definir algoritmos a simular
    algoritmos = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']

    # Crear simulador
    simulador = Simulator(procesos, algoritmos, time_quantum=2)

    # Ejecutar simulaciones
    simulador.run()

    # Visualizar resultados
    simulador.visualize()

if __name__ == "__main__":
    main()
