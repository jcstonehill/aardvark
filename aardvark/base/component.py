from aardvark.base.variables import Variable
from aardvark.base.log import Log

from abc import ABC, abstractmethod

import numpy as np


class Component(ABC):
    component_name = "Component"

    def register(self, name: str):
        self._name = name + " (" + self.component_name + ")"

    def log_message(self, message: str):
        Log.message(self._name +" :: " + message)

    def log_error(self, message: str):
        Log.error(self._name +" :: " + message)

    def check_inputs(self):
        inputs: dict = vars(self.inputs)

        variable: Variable
        for variable in inputs.values():
            if(variable.initial is None):
                self.log_error("Input variable \"" + variable.name + "\" initial value is None.")

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

        outputs: dict = vars(self.outputs)

        variable: Variable
        for variable in outputs.values():
            r2 += variable.r2()

        return np.sqrt(r2)
