import aardvark.internal_api as adv

from abc import ABC, abstractmethod

import numpy as np

class Function(ABC):
    @abstractmethod()
    def solve(self):
        pass

class NusseltNumberCorrelation(Function, ABC):
    @abstractmethod
    def solve(self, Re, Pr):
        """TODO fill this out.
        """
        pass

class FrictionFactorCorrelation(Function, ABC):
    @abstractmethod
    def solve(self, eps, Dh, Re):
        pass

