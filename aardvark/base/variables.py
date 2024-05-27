from aardvark.base.log import Log
from aardvark.mesh.mesh_1d import Mesh1D

from abc import ABC, abstractmethod
from itertools import count

import numpy as np
import matplotlib.pyplot as plt

class Variable(ABC):

    _id = count(0)
    
    @property
    def value(self) -> np.ndarray:
        return self._value
    
    @value.setter
    def value(self, new_value: np.ndarray):
        self.prev_value = self._value

        if(new_value is None):
            self._value = None

        else:
            self._value = np.array(new_value)

    @property
    def initial(self) -> np.ndarray:
        return self._initial
    
    @initial.setter
    def initial(self, new_initial):
        if(new_initial is None):
            self._initial = None

        else:
            self._initial = np.array(new_initial)

    def __init__(self, name: str, initial: np.ndarray = None):
        self.name = name

        self.initial: np.ndarray = initial
        self._value = None
        self.prev_value = None

        self.is_setup = False

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def r2(self) -> float:
        pass

class FloatVar(Variable):
    def setup(self):
        if(not self.is_setup):
            self.value = self.initial

            self.is_setup = True

    def r2(self) -> float:
        return (self.value - self.prev_value)**2

class Mesh1DVar(Variable):
    def __init__(self, name: str, initial: np.ndarray = None, var_type: str = "node"):
        self.name = name

        self.initial: np.ndarray = initial
        self._value = None
        self.prev_value = None

        self.var_type = var_type

        self.is_setup = False

    def setup(self, mesh: Mesh1D):
        if(not self.is_setup):
            self.mesh = mesh

            if(self.var_type != "node" and self.var_type != "cell"):
                Log.error(self.name + " (Mesh1DVar) :: Unrecognized var_type: \"" + self.var_type + "\". Acceptable var_type entries: \"node\" or \"cell\".")
            
            if(self.initial.size == 1):
                if(self.var_type == "node"):
                    self.value = np.array(self.mesh.nodes.size*[self.initial])
                elif(self.var_type == "cell"):
                    self.value = np.array(self.mesh.cells.size*[self.initial])

            else:
                if(self.var_type == "node"):
                    if(self.initial.size != self.mesh.nodes.size):
                        Log.error(self.name + " (Mesh1DVar) :: Initial is an invalid size. initial.size = " + str(self.initial.size) + " and mesh.nodes.size = " + str(self.mesh.nodes.size) + ".")
                elif(self.var_type == "cell"):
                    if(self.initial.size != self.mesh.cells.size):
                        Log.error(self.name + " (Mesh1DVar) :: Initial is an invalid size. initial.size = " + str(self.initial.size) + " and mesh.cells.size = " + str(self.mesh.cells.size) + ".")
                
                self.value = self.initial

            self.is_setup = True

    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)
    
    def plot(self):
        if(self.var_type == "node"):
            x_label = "Node X (m)"
            x = self.mesh.nodes
            
        elif(self.var_type == "cell"):
            x_label = "Cell X (m)"
            x = self.mesh.cells

        plt.xlabel(x_label)
        plt.ylabel(self.name)

        plt.ylim(0, np.max(self.value))

        plt.grid(True)
        plt.tight_layout()

        plt.plot(x, self.value, 'o')
        plt.show()

class FlowStateVar(Variable):
    def setup(self):
        if(not self.is_setup):
            if(len(self.initial != 3)):
                Log.error

            self.value = self.initial

            self.is_setup = True

    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)