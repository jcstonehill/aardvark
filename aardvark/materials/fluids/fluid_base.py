from abc import ABC, abstractmethod
class FluidBase(ABC):
    
    @abstractmethod
    def rho(self, T: float, P: float) -> float:
        pass

    @abstractmethod
    def cp(self, T: float, P: float) -> float:
        pass