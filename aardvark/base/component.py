from aardvark.base import variables
from aardvark.base.log import Log

from abc import ABC, abstractmethod

import numpy as np


class Component(ABC):
    component_type = "Component"

    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, new_mesh):
        self._mesh = new_mesh

        variable: variables.Variable
        for variable in self.variables.values():
            variable.mesh = new_mesh

    def __init__(self):
        self.name = None
        self.variables = None
        self.mesh = None

        self.parameters = None

    def initialize(self, name: str):
        self.name = name

        self.variables = {}
        
        self.declare_variables()

    def log_message(self, message: str):
        Log.message(self.name + " (" + self.component_type + ") :: " + message)

    def log_error(self, message: str):
        Log.error(self.name + " (" + self.component_type + ") :: " + message)

    def check_variable_name(self, name: str):
        if(name in self.variables):
            self.log_error("Tried to add variable named \"" + name + "\" but a variable with that name already exists.")

    def add_flow_state_var(self, name: str, units: str) -> variables.FlowStateVar:
        self.check_variable_name(name)

        variable = variables.FlowStateVar(self.name, name, units)
        self.variables[name] = variable

        return variable
    
    def add_float_var(self, name: str, units: str) -> variables.FloatVar:
        self.check_variable_name(name)

        variable = variables.FloatVar(self.name, name, units)
        self.variables[name] = variable
        
        return variable
    
    def add_mesh1d_var(self, name: str, units: str, var_type: str) -> variables.Mesh1DVar:
        self.check_variable_name(name)

        variable = variables.Mesh1DVar(self.name, name, units, var_type)
        self.variables[name] = variable
        
        return variable

    @abstractmethod
    def declare_variables(self):
        pass

    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def solve(self, dt: float):
        """TODO
        """
        pass

    def residual(self) -> float:
        r2 = 0

        variable: variables.Variable
        for variable in self.variables.values():
            r2 += variable.r2()

        return np.sqrt(r2)

    def check_initials(self):
        variable: variables.Variable
        for variable in self.variables.values():
            variable.check_initial()

    def march(self):
        variable: variables.Variable
        for variable in self.variables.values():
            variable.value = variable.initial
            variable.prev_value = variable.initial