import aardvark.internal_api as adv

from abc import ABC, abstractmethod
from itertools import count

import numpy as np


class DataSet(ABC):
    pass

class Component(ABC):
    _id = count(0)

    @property
    @abstractmethod
    def component_name(self) -> str:
        return "Component"

    def __init__(self, name = None, opts: dict = None):
        id = Component._id
        self.id = id
        next(Component._id)

        if(name is None):
            self.name = "Component " + str(id)

        else:
            self.name = name

        self.define_inputs()
        self.define_setup()
        self.define_outputs()

        self.opts = opts

    @abstractmethod
    def define_inputs(self):
        pass

    @abstractmethod
    def define_setup(self):
        pass

    @abstractmethod
    def define_outputs(self):
        pass

    @abstractmethod
    def solve_steady_state(self):
        """TODO
        """
        pass

        
    def check(self):
        # TODO UPDATE SO THAT EACH COMPONENT CHECKS ITSELF.
        # This function should cast inputs to appropriate aardvark variables (i.e. float -> adv.FloatVar)

        inputs = vars(self.inputs)

        for property, value in inputs.items():
            if(value is None):
                # TODO rewrite error message.
                raise Exception("Error input not connected")
            
            if(type(value) is float):
                inputs[property] = adv.FloatVar(value)

            if(type(value) is int):
                inputs[property] = adv.FloatVar(float(value))

            if(type(value) is list):
                inputs[property] = adv.FloatArrayVar(np.array(value))

            if(type(value) is np.ndarray):
                inputs[property] = adv.FloatArrayVar(value)