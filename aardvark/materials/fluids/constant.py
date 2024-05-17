import aardvark.internal_api as adv

from abc import ABC, abstractmethod
class FluidBase(ABC):
    
    def __init__(self, rho: float, k: float, cp: float, cv: float, mu: float)

    @abstractmethod
    def rho_from_T_P(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def cp_from_T_P(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def mu_from_T_P(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def k_from_T_P(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def e_from_T_P(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def T_from_e_P(self, e: float, P: float) -> float:
        pass