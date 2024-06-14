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

            return

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

    def __init__(self, component_name: str, name: str, units: str = None):
        self.name = name
        self.units = units

        self.component_name = component_name

        self.initial: np.ndarray = None
        self._value: np.ndarray = None
        self.value: np.ndarray = None

        self.mesh = None

    def log_message(self, message: str):
        Log.error(self.component_name + " :: " + self.name + " :: " + message)

    def log_error(self, message: str):
        Log.error(self.component_name + " :: " + self.name + " :: " + message)

    def check_initial(self):
        if(self.initial is None):
            self.log_error("Initial is None.")

    @abstractmethod
    def r2(self) -> float:
        pass

    @abstractmethod
    def update_from(self, source: Variable):
        pass

class FloatVar(Variable):
    def r2(self) -> float:
        return (self.value - self.prev_value)**2
    
    def update_from(self, source: FloatVar):
        if(type(source) is not FloatVar):
            self.log_error("Source is not a FloatVar.")

        self.value = np.copy(source.value)
        self.initial = np.copy(source.initial)

class Mesh1DVar(Variable):

    @property
    def value(self) -> np.ndarray:
        return self._value
    
    @value.setter
    def value(self, value: np.ndarray):
        self.prev_value = self._value

        if(value is None):
            self._value = None

            return

        value = np.array(value)

        if(self.var_type == "node"):
            if(value.size != self.mesh.nodes.size):
                self.log_error("Tried to assign value to an improper size. value.size = " + str(value.size) + " and nodes.size = " + str(self.mesh.nodes.size) + ".")
        
        elif(self.var_type == "cell"):
            if(value.size != self.mesh.cells.size):
                self.log_error("Tried to assign value to an improper size. value.size = " + str(value.size) + " and cells.size = " + str(self.mesh.cells.size) + ".")
        
        self._value = value

    @property
    def initial(self) -> np.ndarray:
        return self._initial
    
    @initial.setter
    def initial(self, initial):
        if(initial is None):
            self._initial = None

        else:
            self._initial = np.array(initial)

    def __init__(self, component_name: str, name: str, units: str, var_type: str = "node"):
        self.name = name
        self.units = units

        self.component_name = component_name

        self.initial: np.ndarray = None
        self._value: np.ndarray = None
        self.value: np.ndarray = None
        
        self.var_type = var_type

        self.mesh: Mesh1D = None

    def check_initial(self):
        if(self.var_type == "node"):
            N = self.mesh.nodes.size

        else:
            N = self.mesh.cells.size

        if(self.initial is None):
            self.log_error("Initial is None.")

        if(self.initial.size == 1):
            self.initial = np.array(N*[self.initial])

        elif(self.initial.size != N):
                self.log_error("Initial is an invalid size. initial.size is \"" + str(self.initial.size) + "\" and required size is \"" + str(self.mesh.nodes.size) + "\".")
            
    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)
    
    def update_from(self, source: Mesh1DVar):
        if(type(source) is not Mesh1DVar):
            self.log_error("Source is not a Mesh1DVar.")

        self.value = np.copy(source.value)
    
    def plot(self):
        if(self.var_type == "node"):
            xlabel = "Node X [m]"
            x = self.mesh.nodes
            
        elif(self.var_type == "cell"):
            xlabel = "Cell X [m]"
            x = self.mesh.cells

        if(self.units is None):
            ylabel = self.name + " [" + self.units + "]"
        
        else:
            ylabel = self.name

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.ylim(0, 1.05*np.max(self.value))

        plt.grid(True)
        plt.tight_layout()

        plt.plot(x, self.value, 'o')
        plt.show()
 
class FlowStateVar(Variable):
    @property
    def value(self) -> np.ndarray:
        return self._value
    
    @value.setter
    def value(self, value: np.ndarray):
        self.prev_value = self._value

        if(value is None):
            self._value = None

            return

        value = np.array(value)

        if(value.size != 3):
            self.log_error("Tried to set value using incorrect size. FlowStateVar.value must be of size 3. (T0, P0, m_dot).")

        self._value = value
            
    def r2(self) -> float:
        return np.sum((self.value - self.prev_value)**2)
    
    def update_from(self, source: FlowStateVar):
        if(type(source) is not FlowStateVar):
            self.log_error("Target is not a FlowStateVar.")

        self.value = np.copy(source.value)
        self.initial = np.copy(source.initial)