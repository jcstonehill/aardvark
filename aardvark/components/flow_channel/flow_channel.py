import aardvark.internal_api as adv

import numpy as np

class FlowChannel1D(adv.ComponentBase):

# https://cardinal.cels.anl.gov/theory/thm.html

    def __init__(self, N: int, A: float, P_wall: float,  L: float, fluid: adv.FluidBase, 
            nu_cor: adv.NuCorrelationBase, ff_cor: adv.FFCorrelationBase, tol = 1e-6, max_iter_per_node = 100):
        """TODO fill this out.
        """
        self.N = N
        self.A = A
        self.P_wall = P_wall
        self.L = L
        self.fluid = fluid
        self.nu_cor = nu_cor
        self.ff_cor = ff_cor

        self.tol = tol
        self.max_iter = max_iter_per_node

        self.Dh = 4*A/P_wall
        self.dx = L/N

    def get_static_conditions(self, T0: float, P0: float, m_dot: float, A: float) -> tuple:
        T = T0
        P = P0

        for _ in range(self.max_iter):
            rho = self.fluid.rho_from_T_P(T, P)
            cp = self.fluid.cp_from_T_P(T, P)

            u = m_dot / (rho*A)

            T_prev = T
            P_prev = P

            T = T0 - u**2/(2*cp)
            P = P0 - 0.5*rho*u**2

            res = np.sqrt(((T-T_prev)/T)**2 + ((P-P_prev)/P)**2)

            if(res < self.max_iter):
                break

        return T, P

    def get_reynolds(self, rho, u, Dh, mu):
        return rho*u*Dh/mu
    
    def get_prandtl(self, cp, mu, k):
        return cp*mu/k

    def solve(self, dt: int):
        """TODO fill this out.
        """
        
        # Get values from input dict
        T0_in = self.inputs["T0_in"]
        P0_in = self.inputs["P0_in"]
        m_dot = self.inputs["m_dot"]
        T_wall_z = self.inputs["T_wall_z"]
        T_wall = self.inputs["T_wall"]

        # Initialize output variables
        # Cell outputs
        cell_z = np.array(self.N)
        Q_dot = np.array(self.N)

        # Node Outputs
        node_z = np.array(self.N+1)
        T = np.array(self.N+1)
        P = np.array(self.N+1)
        rho = np.array(self.N+1)
        u = np.array(self.N+1)
        E = np.array(self.N+1)

        # Scalar Outputs
        m_dot = m_dot
        T0_out = T0_in
        P0_out = P0_in

        # Get Static Conditions
        T_in, P_in = self.get_static_conditions(T0_in, P0_in, m_dot, self.A)

        # Add inlet values to solution arrays
        T[0] = T_in
        P[0] = P_in
        rho[0] = self.fluid.rho_from_T_P(T[0], P[0])
        u[0] = m_dot / (rho[0]*self.A)
        E[0] = self.fluid.e_from_T_P()

        # MAIN LOOP
        for i in range(self.N):
            # Set initial guess for next node
            T[i+1] = T[i]
            P[i+1] = P[i]
            rho[i+1] = rho[i]
            u[i+1] = u[i]
            E[i+1] = E[i]

            # Non-linear loop for conservation equations asdfasdfasdfas asdfasdffas asdfasdfasdf asdf dsasdffa asdfasdf assdffasdf
            for _ in self.max_iter:
                # Mass Conservation
                u[i+1] = rho[i]*u[i]/rho[i+1]

                # Momentum Conservation
                T_avg = (T[i] + T[i+1])/2
                P_avg = (P[i] + P[i+1])/2

                mu = self.fluid.mu_from_T_P(T_avg, P_avg)
                cp = self.fluid.cp_from_T_P(T_avg, P_avg)
                k = self.fluid.k_from_T_P(T_avg, P_avg)

                Re = self.get_reynolds(rho[i+1], u[i+1], self.Dh, mu[i+1])
                Pr = self.get_prandtl(cp[i+1], mu[i+1], k[i+1])

                f = self.ff_cor.ff(Re, Pr)

                rho_avg = (rho[i] + rho[i+1])/2
                u_avg = (u[i] + u[i+1])/2

                C1 = P[i]
                C2 = rho[i]*u[i]**2
                C3 = -rho[i+1]*u[i+1]**2
                C4 = -(f*self.dx*rho_avg*u_avg**2)/(2*self.Dh)
                P[i+1] = C1 + C2 + C3 + C4

                # Energy Equation

                