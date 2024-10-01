from process import Process
from Scheduler import Scheduler
from Simulator import Simulator
import random

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

def convertir_prioridad_a_numero(prioridad):
    if prioridad == 'baja':
        return random.randint(1, 3)
    elif prioridad == 'media':
        return random.randint(4, 7)
    elif prioridad == 'alta':
        return random.randint(8, 10)
    else:
        return random.randint(4, 7)  # Valor por defecto (media)

def agregar_procesos_usuario():
    num_procesos = int(input("¿Cuántos procesos deseas agregar?: "))
    nuevos_procesos = []
    for i in range(num_procesos):
        id_proceso = i + 1  # ID asignado automáticamente
        arrival_time = random.randint(2, 10)  # Tiempo de llegada aleatorio entre 2 y 10
        burst_time = random.randint(1, 10)  # Burst time aleatorio entre 1 y 10

        # Preguntar por la prioridad con validación
        while True:
            prioridad_texto = input(f"Ingrese prioridad del proceso {id_proceso} (baja/media/alta): ").lower()
            if prioridad_texto in ["baja", "media", "alta"]:
                prioridad_numero = convertir_prioridad_a_numero(prioridad_texto)
                break  # Sale del bucle si la prioridad es válida
            else:
                print("Error: La prioridad ingresada no es válida. Inténtalo de nuevo.")

        # Añadir el proceso a la lista
        nuevos_procesos.append(Process(id=id_proceso, arrival_time=arrival_time, burst_time=burst_time, priority=prioridad_numero))
        print(f"Proceso {id_proceso}: llegada={arrival_time}, burst_time={burst_time}, prioridad={prioridad_texto} (valor numérico: {prioridad_numero})")

    return nuevos_procesos

def main():
    print("\nAgrega tus procesos:")
    processes = agregar_procesos_usuario()
    
    algorithms = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']
    simulador = Simulator(processes, algorithms)

    while True:
        opcion = mostrar_menu()

        # Ejecutar el algoritmo seleccionado
        if opcion == 1:
            simulador.run('FIFO')
            simulador.generar_reporte_pdf("FIFO")            
        elif opcion == 2:
            simulador.run('SJF')
            simulador.generar_reporte_pdf("SJF")
        elif opcion == 3:
            simulador.run('Round Robin')
            simulador.generar_reporte_pdf("Round Robin")
        elif opcion == 4:
            simulador.run('Prioridad')
            simulador.generar_reporte_pdf("Prioridad")

        continuar = input("\n¿Deseas ejecutar otro algoritmo? (s/n): ").lower()
        if continuar != 's':
            # Mostrar gráficos al final de todas las simulaciones
            print("\nMostrando gráficos de los algoritmos ejecutados:")
            simulador.visualize()
            break

if __name__ == "__main__":
    main()