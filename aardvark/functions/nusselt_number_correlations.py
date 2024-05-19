import numpy as np


def dittus_boelter(Re: float, Pr: float) -> float:
    """TODO fill this out.
    """
    return np.array(0.023*Re**0.8*Pr**0.4)