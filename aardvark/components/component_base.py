import aardvark.internal_api as adv

from abc import ABC, abstractmethod

class DataSetBase(ABC):
    pass

class ComponentBase(ABC):
    
    @property
    @abstractmethod
    def inputs(self):
        pass

    @property
    @abstractmethod
    def outputs(self):
        pass
    
    @abstractmethod
    def solve(self, dt: int):
        """Solve for the component's solution variables at next timestep.

        Take initial conditions (self.ic), and the inputs (self.inputs), and
        solve for the outputs (self.outputs)

        Parameters
        ----------
        dt : int
            Time step (s)
        """
        pass

    def check(self):
        for property, value in vars(self.inputs).items():
            if(value is None):
                # TODO rewrite error message.
                raise Exception("Error input not connected")