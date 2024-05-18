import aardvark.internal_api as adv

import numpy as np

class ColebrookWhite(adv.FrictionFactorCorrelation):
    def solve(self, eps: float, Dh: float, Re: float) -> float:
        return np.array(1.325*(np.log(eps/(3.7*Dh) + 5.74/(Re**0.9)))**-2)