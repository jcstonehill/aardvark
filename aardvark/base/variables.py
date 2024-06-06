from __future__ import annotations

from aardvark.base.log import Log
from aardvark.mesh.mesh_1d import Mesh1D

from abc import ABC, abstractmethod


import numpy as np
import matplotlib.pyplot as plt

class Variable(ABC):
    
    @property
    def value(self) -> np.ndarray:
        return self._value
    
    @value.setter
    def value(self, value: np.ndarray):
        self.prev_value = self._value

        if(value is None):
            self._value = None

        else:
            self._value = np.array(value)

    @property
    def initial(self) -> np.ndarray:
        return self._initial
    
    @initial.setter
    def initial(self, initial):
        if(initial is None):
            self._initial = None

        else:
            self._initial = np.array(initial)

    def __init__(self, component_name: str, var_name: str, units: str = None, initial: np.ndarray = None):
        self.component_name = component_name
        self.var_name = var_name
        self.units = units

        self.initial: np.ndarray = initial
        self._value = None
        self.prev_value = None

    def log_message(self, message: str):
        Log.error(self.component_name + " :: " + self.var_name + " :: " + message)

    def log_error(self, message: str):
        Log.error(self.component_name + " :: " + self.var_name + " :: " + message)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def r2(self) -> float:
        pass

class FloatVar(Variable):
    def setup(self):
        self.value = self.initial

    def r2(self) -> float:
        return (self.value - self.prev_value)**2

class Mesh1DVar(Variable):
    def __init__(self, component_name: str, var_name: str, units: str, initial: np.ndarray = None, var_type: str = "node"):
        self.component_name = component_name
        self.var_name = var_name
        self.units = units

        self.initial: np.ndarray = initial
        self._value = None
        self.prev_value = None

        self.var_type = var_type

        self.mesh: Mesh1D = None

    def add_mesh(self, mesh: Mesh1D):
        self.mesh = mesh

    def setup(self):
        if(self.var_type != "node" and self.var_type != "cell"):
            self.log_error("Unrecognized var_type: \"" + self.var_type + "\". Acceptable var_type entries: \"node\" or \"cell\".")
        
        if(self.initial.size == 1):
            if(self.var_type == "node"):
                self.value = np.array(self.mesh.nodes.size*[self.initial])
            
            elif(self.var_type == "cell"):
                print(self.var_name)
                self.value = np.array(self.mesh.cells.size*[self.initial])

        else:
            if(self.var_type == "node"):
                if(self.initial.size != self.mesh.nodes.size):
                    self.log_error("Initial is an invalid size. initial.size = " + str(self.initial.size) + " and mesh.nodes.size = " + str(self.mesh.nodes.size) + ".")
            
            elif(self.var_type == "cell"):
                if(self.initial.size != self.mesh.cells.size):
                    self.log_error("Initial is an invalid size. initial.size = " + str(self.initial.size) + " and mesh.cells.size = " + str(self.mesh.cells.size) + ".")
            
            self.value = self.initial

    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)
    
    def plot(self):
        if(self.var_type == "node"):
            xlabel = "Node X [m]"
            x = self.mesh.nodes
            
        elif(self.var_type == "cell"):
            xlabel = "Cell X [m]"
            x = self.mesh.cells

        if(self.units is None):
            ylabel = self.var_name + " [" + self.units + "]"
        
        else:
            ylabel = self.var_name

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.ylim(0, 1.05*np.max(self.value))

        plt.grid(True)
        plt.tight_layout()

        plt.plot(x, self.value, 'o')
        plt.show()
 
class FlowStateVar(Variable):
    def setup(self):
        if(self.initial.size != 3):
            self.log_error("Initial is the wrong size. Must provide 3 values: (T0, P0, mdot).")

        self.value = self.initial

    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)