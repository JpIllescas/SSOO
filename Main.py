import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QInputDialog, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from process import Process
from Simulator import Simulator

class AlgorithmThread(QThread):
    finished_signal = pyqtSignal(str)

    def __init__(self, simulator, algorithm):
        super().__init__()
        self.simulator = simulator
        self.algorithm = algorithm

    def run(self):
        if self.algorithm == 1:
            self.simulator.run('FIFO')
            self.simulator.generar_reporte_pdf("FIFO")
        elif self.algorithm == 2:
            self.simulator.run('SJF')
            self.simulator.generar_reporte_pdf("SJF")
        elif self.algorithm == 3:
            self.simulator.run('Round Robin')
            self.simulator.generar_reporte_pdf("Round Robin")
        elif self.algorithm == 4:
            self.simulator.run('Prioridad')
            self.simulator.generar_reporte_pdf("Prioridad")

        self.finished_signal.emit("El algoritmo ha sido ejecutado y el reporte PDF generado.")

class SchedulerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.processes = []
        self.algorithms = ['FIFO', 'SJF', 'Round Robin', 'Prioridad']
        self.simulador = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simulador de Scheduling con Hilos")
        self.setGeometry(100, 100, 400, 400)

        self.label = QLabel("Selecciona el algoritmo de scheduling:", self)
        self.label.setGeometry(50, 50, 300, 20)

        self.btn_fifo = QPushButton("FIFO", self)
        self.btn_fifo.setGeometry(50, 100, 100, 30)
        self.btn_fifo.clicked.connect(lambda: self.run_algorithm_thread(1))

        self.btn_sjf = QPushButton("SJF", self)
        self.btn_sjf.setGeometry(150, 100, 100, 30)
        self.btn_sjf.clicked.connect(lambda: self.run_algorithm_thread(2))

        self.btn_rr = QPushButton("Round Robin", self)
        self.btn_rr.setGeometry(50, 150, 100, 30)
        self.btn_rr.clicked.connect(lambda: self.run_algorithm_thread(3))

        self.btn_priority = QPushButton("Prioridad", self)
        self.btn_priority.setGeometry(150, 150, 100, 30)
        self.btn_priority.clicked.connect(lambda: self.run_algorithm_thread(4))

        self.btn_add_process = QPushButton("Agregar Procesos", self)
        self.btn_add_process.setGeometry(50, 200, 200, 30)
        self.btn_add_process.clicked.connect(self.agregar_procesos_usuario)

        self.btn_update_graph = QPushButton("Actualizar Gráfica", self)
        self.btn_update_graph.setGeometry(50, 250, 200, 30)
        self.btn_update_graph.clicked.connect(self.update_graph)
        self.btn_update_graph.setEnabled(False)  # Deshabilitar inicialmente

        self.btn_reset_graph = QPushButton("Reiniciar Gráfica", self)
        self.btn_reset_graph.setGeometry(50, 300, 200, 30)
        self.btn_reset_graph.clicked.connect(self.reset_graph)

        self.show()

    def convertir_prioridad_a_numero(self, prioridad):
        if prioridad == 'baja':
            return random.randint(1, 3)
        elif prioridad == 'media':
            return random.randint(4, 7)
        elif prioridad == 'alta':
            return random.randint(8, 10)
        else:
            return random.randint(4, 7)  # Valor por defecto (media)

    def agregar_procesos_usuario(self):
        num_procesos, ok = QInputDialog.getInt(self, "Agregar Procesos", "¿Cuántos procesos deseas agregar?:", 1, 1)
        if ok:
            for i in range(num_procesos):
                id_proceso = i + 1  # ID asignado automáticamente
                arrival_time = random.randint(2, 10)  # Tiempo de llegada aleatorio
                burst_time = random.randint(1, 10)  # Burst time aleatorio

                prioridad_texto, ok = QInputDialog.getText(self, f"Proceso {id_proceso}",
                                                           f"Ingrese prioridad del proceso {id_proceso} (baja/media/alta):")
                if ok:
                    prioridad_numero = self.convertir_prioridad_a_numero(prioridad_texto.lower())
                    proceso = Process(id=id_proceso, arrival_time=arrival_time, burst_time=burst_time, priority=prioridad_numero)
                    self.processes.append(proceso)
                    QMessageBox.information(self, "Proceso Agregado",
                                            f"Proceso {id_proceso}: llegada={arrival_time}, burst_time={burst_time}, prioridad={prioridad_texto} (valor numérico: {prioridad_numero})")

            self.simulador = Simulator(self.processes, self.algorithms)

    def run_algorithm_thread(self, opcion):
        if not self.simulador:
            QMessageBox.warning(self, "Error", "Debes agregar procesos primero.")
            return
        
        # Crear y conectar el hilo
        self.thread = AlgorithmThread(self.simulador, opcion)
        self.thread.finished_signal.connect(self.on_algorithm_finished)
        self.thread.start()

    def on_algorithm_finished(self, message):
        QMessageBox.information(self, "Algoritmo Ejecutado", message)
        self.btn_update_graph.setEnabled(True)  # Habilitar el botón de actualizar gráfica

    def update_graph(self):
        if self.simulador:
            self.simulador.visualize()
        else:
            QMessageBox.warning(self, "Error", "No hay datos para visualizar.")

    def reset_graph(self):
        # Limpiar los datos de los procesos y el simulador
        self.processes = []
        self.simulador = None
        self.btn_update_graph.setEnabled(False)  # Deshabilitar el botón de actualizar gráfica
        QMessageBox.information(self, "Gráfica Reiniciada", "Los datos han sido reiniciados. Puedes agregar nuevos procesos.")

def main():
    app = QApplication(sys.argv)
    ex = SchedulerApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
