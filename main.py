import sys
import random
import numpy as np
from numpy.random import default_rng
import scipy.stats
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QSpinBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
)
from PyQt6.QtGui import QFont

rng = default_rng()

class Client:
    timeProcess: int = None
    timeInQueue: int = None
    def __init__(self):
        self.timeProcess = int(max(rng.exponential(12), 1))
        self.timeInQueue = 0

class Operator:
    name: str = None
    currentClient: Client = None
    Nofclients: int = None
    averageTime: float = None
    def __init__(self, name: str):
        self.name = name
        self.Nofclients = 0
        self.averageTime = 0
    def accept(self, client: Client):
        self.currentClient = client
        self.Nofclients += 1
        self.averageTime = (self.averageTime * (self.Nofclients - 1) + client.timeInQueue) / self.Nofclients
    def process(self):
        if self.currentClient == None: return
        self.currentClient.timeProcess -= 1
        if self.currentClient.timeProcess <= 0:
            self.currentClient = None

class Queue:
    queue: list[Client] = []
    time: int = None
    maxLen: int = None
    def __init__(self):
        self.queue.append(Client())
        self.time = rng.poisson(len(self.queue))
        self.maxLen = 1
    def run(self):
        for pers in self.queue:
            pers.timeInQueue += 1

        self.time -= 1
        if self.time <= 0:
            self.queue.append(Client())
            self.maxLen = max(len(self.queue), self.maxLen)
            self.time = rng.poisson(len(self.queue))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Симулятор очереди банка')

        panel = QHBoxLayout()
        # start button
        start_button = QPushButton("СТАРТ")
        start_button.clicked.connect(self.start)

        self.timer = QTimer()
        stop_button = QPushButton("СТОП")
        stop_button.clicked.connect(self.stop)
        panel.addWidget(start_button)
        panel.addWidget(stop_button)

        # processing area
        self.area = QGridLayout()

        # queue
        self.display = QFormLayout()
        
        layout = QVBoxLayout()
        layout.addLayout(panel)
        layout.addLayout(self.area)
        layout.addLayout(self.display)
        root = QWidget()
        root.setLayout(layout)
        self.setCentralWidget(root)

    def start(self):
        self.q = Queue()
        self.display.addRow(QLabel(f'Клиент: {self.q.queue[0].timeProcess}, в очереди: {self.q.queue[0].timeInQueue}'))
        self.ops: list[Operator] = [Operator('Alex'), Operator('Brunhilda'), Operator('Crissy'), Operator('Dan')]
        for index, op in enumerate(self.ops):
            self.area.addWidget(QLabel(f'{op.name}'), 1, index)
        
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.run)
        self.timer.start()

    def run(self):
        pass
    def stop(self):
        self.timer.stop()


random.seed()
app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()
