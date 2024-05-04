from abc import ABC, abstractmethod

class _ComponentBase(ABC):
    def solve(ic: dict, con: dict, dt: int, sol: dict):
        """Solve for the component's solution variables at next timestep.

        Takes values from ic dictionary and performs calculations to determine
        the solution after dt time.

        Parameters
        ----------
        ic : dict
            The initial conditions. This component's solution dictionary before
            time progression.

        con : dict
            Connections. 

        dt : int
            Time step (s). If -1, then solve for steady state.

        sol : dict
            Solution set. 

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a parameter.
        """
        pass