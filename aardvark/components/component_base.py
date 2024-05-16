from abc import ABC, abstractmethod

class ComponentInputs(ABC):
    @abstractmethod
    def initialize_variables(self):
        pass

class ComponentOutputs(ABC):
    @abstractmethod
    def initialize_variables(self):
        pass

class ComponentBase(ABC):

    @property
    def 

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