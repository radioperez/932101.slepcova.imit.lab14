from numpy.random import default_rng


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

q = Queue()
ops: list[Operator] = [Operator('Alex'), Operator('Brunhilda'), Operator('Crissy'), Operator('Dan')]

for t in range(10000):
    freeops = [op for op in ops if op.currentClient == None]
    for op in freeops:
        if len(q.queue) == 0: continue
        op.accept(q.queue.pop())
    for op in ops:
        op.process()
    q.run()
    print(f'Queue length: {len(q.queue)}')

for op in ops:
    print(f'{op.name}: {op.Nofclients}, {op.averageTime: .3f}')
print(f'Max queue length: {q.maxLen}')
