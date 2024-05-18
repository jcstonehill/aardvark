import aardvark.internal_api as adv

from abc import ABC, abstractmethod
from itertools import count

import numpy as np

class Variable(ABC):
    _id = count(0)

    def __init__(self, init_val):
        id = Variable._id
        self.id = id
        next(Variable._id)
        
        if(self.val_is_valid(init_val)):
            self._val = init_val
            self._prev_val = None

            adv.variables.append(self)

    def set(self, val):
        self._prev_val = self._val
        self._val = val

    def get(self):
        return self._val
    
    @abstractmethod
    def r2(self) -> float:
        pass

    @abstractmethod
    def val_is_valid(self, var) -> bool:
        pass

class NoneVar(Variable):
    def __init__(self):
        self._val = None

    def set(self, val):
        pass

    def r2(self) -> float:
        return None

    def val_is_valid(self, val) -> bool:
        return True

class FloatVar(Variable):
    def r2(self) -> float:
        if(self._prev_val is None):
            return None
        
        return (self._val - self._prev_val)**2
    
    def val_is_valid(self, val) -> bool:
        if(type(val) is not float):
            raise Exception("Aardvark: Variable " + str(self._id) + ": Invalid type assigned. Expected float. Received " + str(type(val)) + ".")
        
        return True
    
class FloatArrayVar(Variable):
    def r2(self) -> float:
        if(self._prev_val is None):
            return None
        
        return (self._val - self._prev_val)**2
        
    def val_is_valid(self, val) -> bool:
        if(type(val) is not np.ndarray):
            raise Exception("Aardvark: Variable " + str(self._id) + ": Invalid type assigned. Expected np.ndarray. Received " + str(type(val)) + ".")
        
        return True