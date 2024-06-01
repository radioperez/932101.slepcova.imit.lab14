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
    label: QLabel = None
    def __init__(self):
        self.timeProcess = int(max(rng.exponential(12), 1))
        self.timeInQueue = 0
        self.label = QLabel(f'Клиент: {self.timeProcess}, в очереди: {self.timeInQueue}')

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
        self.currentClient.label.setText(f'Клиент: {self.currentClient.timeProcess}, у оператора: {self.name}')
        self.currentClient.label.update()
        if self.currentClient.timeProcess <= 0:
            self.currentClient.label.deleteLater()
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
            pers.label.setText(f'Клиент: {pers.timeProcess}, в очереди: {pers.timeInQueue}')
            pers.label.update()

        self.time -= 1
        if self.time <= 0:
            self.queue.append(Client())
            self.maxLen = max(len(self.queue), self.maxLen)
            self.time = rng.poisson(len(self.queue))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Симулятор очереди банка')
        self.setMinimumWidth(900)

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
        self.display.addRow(self.q.queue[-1].label)
        self.ops: list[Operator] = [Operator('Александра'), Operator('Бронеслава'), Operator('Валерия'), Operator('Дан')]
        for index, op in enumerate(self.ops):
            oplabel = QLabel(f'{op.name}')
            oplabel.setStyleSheet('font-weight: 600;')
            self.area.addWidget(oplabel, 0, index)
        
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.run)
        self.timer.start()

    def run(self):
        freeops = [op for op in self.ops if op.currentClient == None]
        for index, op in enumerate(freeops):
            if len(self.q.queue) == 0: continue
            person = self.q.queue.pop()
            op.accept(person)
            person.label.setText(f'Клиент: {person.timeProcess}, у оператора: {op.name}')
            self.display.update()
        for index, op in enumerate(self.ops):
            op.process()
            self.display.update()
        self.q.run()
        for person in self.q.queue:
            self.display.addRow(person.label)
        
    def stop(self):
        self.timer.stop()
        for index, op in enumerate(self.ops):
            stat = QLabel(f'{op.Nofclients} клиентов,\nсреднее время\nожидания: {op.averageTime:.2f}')
            self.area.addWidget(stat, 1, index)
        for person in self.q.queue: person.label.deleteLater()
        self.q.queue = []


random.seed()
app = QApplication(sys.argv)
app.setStyleSheet("QLabel {font-size: 20px; text-align: center;} QPushButton {font-size: 20px;}")
main = MainWindow()
main.show()
app.exec()
