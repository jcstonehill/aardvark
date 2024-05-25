from abc import ABC, abstractmethod

class Mesh(ABC):
    def __init__(self):
        self.nodes = None
        self.cells = None

    @abstractmethod
    def setup(self):
        pass
