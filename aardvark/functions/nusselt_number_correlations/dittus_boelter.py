import aardvark.internal_api as adv

import numpy as np


class DittusBoelter(adv.NusseltNumbercorrelation):
    def solve(self, Re: float, Pr: float) -> float:
        """TODO fill this out.
        """
        return np.array(0.023*Re**0.8*Pr**0.4)