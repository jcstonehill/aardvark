import aardvark.internal_api as adv

from abc import ABC, abstractmethod

import numpy as np

class DataSetBase(ABC):
    pass

class ComponentBase(ABC):
    
    def __init__(self):
        self.inputs = DataSetBase()
        self.opt_inputs = DataSetBase()
        self.outputs = DataSetBase()

    @abstractmethod
    def solve_steady_state(self):
        """TODO
        """
        pass

    def check(self):

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

        opt_inputs = vars(self.opt_inputs)

        for property, value in opt_inputs.items():
            if(value is None):
                opt_inputs[property] = adv.NoneVar()

            if(type(value) is list):
                opt_inputs[property] = adv.FloatArrayVar(np.array(value))