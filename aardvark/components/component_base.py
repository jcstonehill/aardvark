from abc import ABC, abstractmethod

class ComponentBase(ABC):

    @property
    @abstractmethod
    def inputs(self) -> dict:
        """TODO fill this out.
        """
        pass

    @property
    @abstractmethod
    def outputs(self) -> dict:
        """TODO fill this out.
        """
        pass

    @property
    @abstractmethod
    def ic(self) -> dict:
        """TODO fill this out.
        """
        pass

    @abstractmethod
    def solve(self, dt: int):
        """Solve for the component's solution variables at next timestep.

        Take initial conditions (self.ic), and the inputs (self.inputs), and
        solve for the outputs (self.outputs)

        Parameters
        ----------
        dt : int
            Time step (s). If -1, then solve for steady state.
        """
        pass