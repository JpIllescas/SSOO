from process import Process
from Scheduler import Scheduler  # Importa las clases necesarias
from Simulator import Simulator

# Simulación de cada algoritmo
def ejecutar_FIFO(procesos):
    simulator = Simulator(procesos, ["FIFO"])  # Configuramos el simulador para FIFO
    simulator.run("FIFO")  # Ejecutamos la simulación con el algoritmo FIFO
    return simulator  # Retornamos el simulador para guardar métricas

def ejecutar_SJF(procesos):
    simulator = Simulator(procesos, ["SJF"])  # Configuramos el simulador para SJF
    simulator.run("SJF")  # Ejecutamos la simulación con el algoritmo SJF
    return simulator

def ejecutar_RoundRobin(procesos):
    simulator = Simulator(procesos, ["Round Robin"], time_quantum=2)  # Configuramos el simulador para Round Robin
    simulator.run("Round Robin")  # Ejecutamos la simulación con el algoritmo Round Robin
    return simulator

def ejecutar_Prioridad(procesos):
    simulator = Simulator(procesos, ["Prioridad"])  # Configuramos el simulador para Prioridad
    simulator.run("Prioridad")  # Ejecutamos la simulación con el algoritmo de Prioridad
    return simulator

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
    # Pedir nivel de rendimiento
    print("Selecciona el nivel de rendimiento:")
    print("1. Alto")
    print("2. Medio")
    print("3. Bajo")
    nivel_rendimiento = int(input("Ingresa el número del nivel de rendimiento que deseas usar: "))

    # Crear procesos de ejemplo (esto deberías adaptarlo según tu proyecto)
    procesos = [Process(1, 0, 10, 1), Process(2, 5, 8, 2), Process(3, 10, 7, 3), Process(4, 15, 6, 1), Process(5, 20, 9, 2)]

    simuladores = []

    while True:
        # Mostrar menú para seleccionar el algoritmo
        algoritmo = mostrar_menu()

        # Ejecutar el algoritmo seleccionado
        if algoritmo == 1:
            simuladores.append(ejecutar_FIFO(procesos))
        elif algoritmo == 2:
            simuladores.append(ejecutar_SJF(procesos))
        elif algoritmo == 3:
            simuladores.append(ejecutar_RoundRobin(procesos))
        elif algoritmo == 4:
            simuladores.append(ejecutar_Prioridad(procesos))

        # Preguntar qué hacer después de la simulación
        otra_opcion = input("\n¿Qué deseas hacer a continuación?\n1. Ejecutar otro algoritmo\n2. Graficar resultados\n3. Terminar\nSelecciona una opción (1/2/3): ").lower()

        if otra_opcion == '2':  # Graficar resultados
            for simulador in simuladores:
                simulador.visualize()
            break
        elif otra_opcion == '3':  # Terminar
            print("Finalizando la ejecución.")
            break

if __name__ == "__main__":
    main()
