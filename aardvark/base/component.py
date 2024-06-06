from aardvark.base.variables import Variable
from aardvark.base.log import Log

from abc import ABC, abstractmethod

import numpy as np


class Component(ABC):
    component_type = "Component"

    def __init__(self, name: str):
        self._name = name

        self.inputs = None
        self.outputs = None

    def register(self, name: str):
        self._name = name

    def log_message(self, message: str):
        Log.message(self._name + " (" + self.component_type + ") :: " + message)

    def log_error(self, message: str):
        Log.error(self._name + " (" + self.component_type + ") :: " + message)

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
