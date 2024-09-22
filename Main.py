from process import Process
from Scheduler import Scheduler
from Simulator import Simulator

def mostrar_menu():
    print("\nSelecciona el algoritmo de scheduling:")
    print("1. FIFO")
    print("2. SJF")
    print("3. Round Robin")
    print("4. Prioridad")
    
    while True:
        opcion = input("Ingresa el número del algoritmo que deseas ejecutar: ")
        if opcion in ['1', '2', '3', '4']:
            return int(opcion)
        else:
            print("Opción no válida. Por favor, selecciona un número entre 1 y 4.")

def main():
    # Crear procesos de ejemplo
    processes = [
        Process(id=1, arrival_time=0, burst_time=5),
        Process(id=2, arrival_time=3, burst_time=9),
        Process(id=3, arrival_time=4, burst_time=6),
    ]

    algorithms = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']
    simulador = Simulator(processes, algorithms)

    while True:
        opcion = mostrar_menu()

        # Ejecutar el algoritmo seleccionado
        if opcion == 1:
            simulador.run('FIFO')
        elif opcion == 2:
            simulador.run('SJF')
        elif opcion == 3:
            simulador.run('Round Robin')
        elif opcion == 4:
            simulador.run('Prioridad')

        continuar = input("\n¿Deseas ejecutar otro algoritmo? (s/n): ").lower()
        if continuar != 's':
            # Mostrar gráficos al final de todas las simulaciones
            print("\nMostrando gráficos de los algoritmos ejecutados:")
            simulador.visualize()
            break

if __name__ == "__main__":
    main()
