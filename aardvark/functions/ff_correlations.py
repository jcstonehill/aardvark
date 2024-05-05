from abc import ABC, abstractmethod

import numpy as np

class FFCorrelationBase(ABC):
    @abstractmethod
    def ff(Re, Pr):
        pass

class ColebrookWhiteFFCorrelation(FFCorrelationBase):
    def ff(eps, Dh, Re):
        return 1.325*(np.log(eps/(3.7*Dh) + 5.74/(Re**0.9)))**-2