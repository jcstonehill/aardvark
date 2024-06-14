from aardvark.base.fluid import Fluid

import numpy as np

def stagnation_to_static_flow(T0: float, P0: float, m_dot: float, A: float, 
              fluid: Fluid, max_iter: int = 100, tol: float = 1e-6) -> tuple:
    
    # Initial guess at T and P
    T = T0
    P = P0

    for _ in range(max_iter):
        rho = fluid.rho_from_T_P(T, P)
        cp = fluid.cp_from_T_P(T, P)

        u = m_dot / (rho*A)

        T_prev = T
        P_prev = P

        T = T0 - u**2/(2*cp)
        P = P0 - 0.5*rho*u**2

        res = np.sqrt((T-T_prev)**2 + (P-P_prev)**2)

        if(res < tol):
            return np.array(T), np.array(P)

    # TODO replace with logging system
    raise Exception("StagnationToStaticFlow not converged")
    
def static_to_stagnation_flow(T: float, P: float, m_dot: float, A: float, fluid: Fluid) -> tuple:
    rho = fluid.rho_from_T_P(T, P)
    cp = fluid.cp_from_T_P(T, P)

    u = m_dot / rho*A

    T0 = T + u**2/(2*cp)
    P0 = P + 0.5*rho*u**2

    return np.array(T0), np.array(P0)