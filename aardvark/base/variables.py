import aardvark.internal_api as adv

from abc import ABC, abstractmethod
from itertools import count

class Variable(ABC):

    _id = count(0)
    
    @property
    def value(self) -> adv.np.ndarray:
        return self._value
    
    @value.setter
    def value(self, new_value: adv.np.ndarray):
        self.prev_value = self._value

        if(new_value is None):
            self._value = None

        else:
            self._value = adv.np.array(new_value)

    @property
    def initial(self) -> adv.np.ndarray:
        return self._initial
    
    @initial.setter
    def initial(self, new_initial):
        if(new_initial is None):
            self._initial = None

        else:
            self._initial = adv.np.array(new_initial)

    def __init__(self, name: str, initial: adv.np.ndarray = None):
        self.name = name

        self.initial: adv.np.ndarray = initial
        self._value = None
        self.prev_value = None

        self.is_initialized = False

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def r2(self) -> float:
        pass

class FloatVar(Variable):
    def initialize(self):
        if(not self.is_initialized):
            self.value = self.initial

            self.is_initialized = True

    def r2(self) -> float:
        return (self.value - self.prev_value)**2

class Mesh1DVar(Variable):
    def initialize(self, x: adv.np.ndarray):
        if(not self.is_initialized):
            self.x = x

            if(self.initial.size == 1):
                self.value = adv.np.array(len(x)*[self.initial])

            else:
                self.value = self.initial

            self.is_initialized = True

    def r2(self) -> float:
        return sum((self.value - self.prev_value)**2)
    
    def plot(self):
        adv.plt.xlabel("Node X (m)")
        adv.plt.ylabel(self.name)
        adv.plt.grid(True)
        adv.plt.tight_layout()

        adv.plt.plot(self.x, self.value)
        adv.plt.show()
