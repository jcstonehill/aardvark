from abc import ABC, abstractmethod
class FluidBase(ABC):
    
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