import aardvark as adv

from abc import ABC, abstractmethod
from itertools import count

import numpy as np

class VarBase(ABC):

    _id = count(0)

    def __init__(self, init_val):
        self.is_connected = False
        self._val = init_val

    def set(self, val):
        self._prev_val = self._val
        self._val = val

    def get(self):
        return self._val
    
    @abstractmethod
    def val_is_valid(self) -> bool:
        pass

class FloatVar(VarBase):
    def val_is_valid(self, val):
        if(type(val) is not float):
            raise Exception("Aardvark: Variable " + str(self._id) + ": Invalid type assigned. Expected float. Received " + str(type(val)) + ".")

class FloatArrayVar(VarBase):
    def val_is_valid(self, val):
        if(type(val) is not np.ndarray):
            raise Exception("Aardvark: Variable " + str(self._id) + ": Invalid type assigned. Expected np.ndarray. Received " + str(type(val)) + ".")