from process import Process
from Simulator import Simulator

def mostrar_menu():
    print("\nSelecciona el algoritmo de scheduling:")
    print("1. FIFO")
    print("2. SJF")
    print("3. Round Robin")
    print("4. Prioridad")
    return input("Ingresa el número del algoritmo que deseas ejecutar: ")

def ejecutar_simulacion(simulador, algoritmo):
    algoritmos = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']
    simulador.run(algoritmos[algoritmo - 1])

def main():
    # Definir procesos con tiempos de llegada variados para crear competencia
    processes = [
        Process(id=1, arrival_time=0, burst_time=5),   # Proceso 1 llega al inicio
        Process(id=2, arrival_time=1, burst_time=3),   # Proceso 2 llega mientras Proceso 1 está ejecutándose
        Process(id=3, arrival_time=4, burst_time=4),   # Proceso 3 llega durante la ejecución del Proceso 2
        Process(id=4, arrival_time=6, burst_time=2),   # Proceso 4 llega casi al final del Proceso 3
    ]

    algorithms = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']
    simulador = Simulator(processes, algorithms)



    while True:
        opcion = mostrar_menu()

        if opcion in ['1', '2', '3', '4']:
            ejecutar_simulacion(simulador, int(opcion))

            # Preguntar si desea realizar otra simulación
            continuar = input("¿Deseas ejecutar otro algoritmo? (s/n): ").lower()
            if continuar == 'n':
                # Preguntar si desea ver los gráficos
                graficar = input("¿Deseas ver los gráficos? (s/n): ").lower()
                if graficar == 's':
                    simulador.visualize()
                break  # Salir del programa
        else:
            print("Opción no válida. Por favor ingresa un número válido (1-4).")

if __name__ == "__main__":
    main()
