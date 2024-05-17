from abc import ABC, abstractmethod

class NuCorrelationBase(ABC):
    @abstractmethod
    def Nu(self, Re, Pr):
        """TODO fill this out.
        """
        pass

class DittusBoelterNuCorrelation(NuCorrelationBase):
    def Nu(self, Re, Pr):
        """TODO fill this out.
        """
        return 0.023*Re**0.8*Pr**0.4