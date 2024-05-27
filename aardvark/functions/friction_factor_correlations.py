import numpy as np
import scipy.optimize


def laminar_friction_factor(Re: float) -> float:
    return np.array(64/Re)

def churchill(eps, Dh, Re):
    a = (2.457*np.log(1/((7/Re)**0.9 + (0.27*eps/Dh))))**16
    b = (37530/Re)**16

    f = 8*((8/Re)**12 + (1/((a+b)**1.5)))**(1/12)

    return f
