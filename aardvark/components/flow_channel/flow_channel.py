import aardvark as adv

import numpy as np

class FlowChannel1D(adv.ComponentBase):

# https://cardinal.cels.anl.gov/theory/thm.html

    inputs = {
        "T0_in"     :   300,
        "P0_in"     :   101325,
        "m_dot"     :   0.0008,
        "T_wall_z"  :   [0.5],
        "T_wall"    :   [300]
    }

    outputs = {
        "cell_z"    :   [0.5],
        "Q_dot"     :   [0],
        "ff_flow"   :   [None],
        "Nu_flow"   :   [None],
        "node_z"    :   [0, 1],
        "Re_flow"   :   [None, None],
        "T_flow"    :   [300, 300],
        "P_flow"    :   [101325, 101325],
        "rho_flow"  :   [None, None],
        "v_flow"    :   [None, None],
        "cp_flow"   :   [None, None],
        "m_dot"     :   0.0008,
        "T0_out"    :   300,
        "P0_out"    :   101325
    }

    ic = {
        
    }

    def __init__(self, N: int, A: float,  L: float, fluid: adv.FluidBase, 
            nu_cor: adv.NuCorrelationBase, ff_cor: adv.FFCorrelationBase, fp_tol = 1e-6, max_fp_iter = 100):
        """TODO fill this out.
        """
        self.N = N
        self.A = A
        self.L = L
        self.fluid = fluid
        self.nu_cor = nu_cor
        self.ff_cor = ff_cor

        self.fp_tol = fp_tol
        self.max_fp_iter = max_fp_iter

    def get_static_conditions(self, T0: float, P0: float, m_dot: float, A: float) -> tuple:
        T = T0
        P = P0

        for _ in range(self.max_fp_iter):
            rho = self.fluid.rho(T, P)
            cp = self.fluid.cp(T, P)

            v = m_dot / (rho*A)

            T_prev = T
            P_prev = P

            T = T0 - v**2/(2*cp)
            P = P0 - 0.5*rho*v**2

            res = np.sqrt(((T-T_prev)/T)**2 + ((P-P_prev)/P)**2)

            if(res < self.fp_tol):
                break

        return T, P, v



        

    def solve(self, dt: int):
        """TODO fill this out.
        """
        
        T0_in = self.inputs["T0_in"]
        P0_in = self.inputs["P0_in"]
        m_dot = self.inputs["m_dot"]
        T_wall_z = self.inputs["T_wall_z"]
        T_wall = self.inputs["T_wall"]

        T_in, P_in = self.get_static_conditions(T0_in, P0_in, m_dot, self.A)

        T_flow = np.array(self.N+1)
        P_flow = np.array(self.N+1)

        T_flow[0] = T_in
        P_flow[0] = P_in

        for _ in range