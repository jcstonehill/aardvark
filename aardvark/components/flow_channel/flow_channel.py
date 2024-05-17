import aardvark.internal_api as adv

import numpy as np

class FlowChannel1DInputs(adv.DataSetBase):
    def __init__(self):
        self.T0_in: adv.FloatVar = None
        self.P0_in: adv.FloatVar = None
        self.m_dot: adv.FloatVar = None

        self.T_wall: adv.FloatArrayVar = None

class FlowChannel1DOutputs(adv.DataSetBase):
    def __init__(self):
        self.T0_out: adv.FloatVar = adv.FloatVar()
        self.P0_out: adv.FloatVar = adv.FloatVar()
        self.m_dot: adv.FloatVar = adv.FloatVar()

        self.node_x: adv.FloatArrayVar = adv.FloatArrayVar()

        self.T: adv.FloatArrayVar = adv.FloatArrayVar()
        self.P: adv.FloatArrayVar = adv.FloatArrayVar()
        self.u: adv.FloatArrayVar = adv.FloatArrayVar()
        self.e: adv.FloatArrayVar = adv.FloatArrayVar()
        self.E: adv.FloatArrayVar = adv.FloatArrayVar()
        
        self.rho: adv.FloatArrayVar = adv.FloatArrayVar()
        self.mu: adv.FloatArrayVar = adv.FloatArrayVar()
        self.cp: adv.FloatArrayVar = adv.FloatArrayVar()
        self.cv: adv.FloatArrayVar = adv.FloatArrayVar()
        self.k: adv.FloatArrayVar = adv.FloatArrayVar()

        self.Re: adv.FloatArrayVar = adv.FloatArrayVar()
        self.Pr: adv.FloatArrayVar = adv.FloatArrayVar()

        self.ff: adv.FloatArrayVar = adv.FloatArrayVar()
        self.Nu: adv.FloatArrayVar = adv.FloatArrayVar()
        self.htc: adv.FloatArrayVar = adv.FloatArrayVar()

class FlowChannel1D(adv.ComponentBase):

# https://cardinal.cels.anl.gov/theory/thm.html

    def __init__(self, N: int, A: float, P_wall: float,  L: float, fluid: adv.FluidBase, 
            Nu_cor: adv.NuCorrelationBase, ff_cor: adv.FFCorrelationBase, tol = 1e-6, max_iter_per_node = 100):
        """TODO fill this out.
        """
        self.inputs: FlowChannel1DInputs = FlowChannel1DInputs()
        self.outputs: FlowChannel1DOutputs = FlowChannel1DOutputs()

        self.N = N
        self.A = A
        self.P_wall = P_wall
        self.L = L
        self.fluid = fluid
        self.Nu_cor = Nu_cor
        self.ff_cor = ff_cor

        self.tol = tol
        self.max_iter = max_iter_per_node

        self.Dh = 4*A/P_wall
        self.dx = L/N
        self.outputs.node_x.set(np.linspace(0, L, N+1))

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

    def solve_steady_state(self):
        # Inputs
        T0_in = self.inputs.T0_in
        P0_in = self.inputs.P0_in
        m_dot = self.inputs.m_dot
        T_wall = self.inputs.T_wall

        # Outputs
        T = np.array(self.N+1)
        P = np.array(self.N+1)

        rho = np.array(self.N+1)
        mu = np.array(self.N+1)
        cp = np.array(self.N+1)
        cv = np.array(self.N+1)
        k = np.array(self.N+1)

        u = np.array(self.N+1)
        e = np.array(self.N+1)
        E = np.array(self.N+1)

        Re = np.array(self.N+1)
        Pr = np.array(self.N+1)

        ff = np.array(self.N+1)
        Nu = np.array(self.N+1)
        htc = np.array(self.N+1)

        # Get Static Conditions
        T_in, P_in = self.get_static_conditions(T0_in, P0_in, m_dot, self.A)

        # Add inlet values to variable arrays
        T[0] = T_in
        P[0] = P_in

        rho[0] = self.fluid.rho_from_T_P(T[0], P[0])
        mu[0] = self.fluid.mu_from_T_P(T[0], P[0])
        cp[0] = self.fluid.cp_from_T_P(T[0], P[0])
        cv[0] = self.fluid.cv_from_T_P(T[0], P[0])
        k[0] = self.fluid.k_from_T_P(T[0], P[0])

        u[0] = m_dot / (rho[0]*self.A)
        e[0] = cv[0]*T[0]
        E[0] = e[0] + 0.5*u[0]**2

        Re[0] = self.get_reynolds(rho[0], u[0], self.Dh, mu[0])
        Pr[0] = self.get_prandtl(cp[0], mu[0], k[0])

        ff[0] = self.ff_cor.ff(Re[0], Pr[0])
        Nu[0] = self.Nu_cor.Nu(Re[0], Pr[0])
        htc[0] = Nu[0] * k[0] / self.Dh

        # MAIN LOOP
        for i in range(self.N):
            # Set initial guess for next node
            T[i+1] = T[i]
            P[i+1] = P[i]

            rho[i+1] = rho[i]
            mu[i+1] = mu[i]
            cp[i+1] = cp[i]
            cv[i+1] = cp[i]
            k[i+1] = k[i]

            u[i+1] = u[i]
            e[i+1] = e[i]
            E[i+1] = E[i]

            Re[i+1] = Re[i]
            Pr[i+1] = Pr[i]

            ff[i+1] = ff[i]
            Nu[i+1] = Nu[i]
            htc[i+1] = htc[i]

            # Non-linear loop for conservation equations
            for _ in self.max_iter:

                # Mass Conservation
                u_new = rho[i]*u[i]/rho[i+1]
                mass_res = (u[i+1] - u_new)**2

                u[i+1] = u_new

                # Momentum Conservation
                mu[i+1] = self.fluid.mu_from_T_P(T[i+1], P[i+1])
                cp[i+1] = self.fluid.cp_from_T_P(T[i+1], P[i+1])
                cv[i+1] = self.fluid.cv_from_T_P(T[i+1], P[i+1])
                k[i+1] = self.fluid.k_from_T_P(T[i+1], P[i+1])

                Re[i+1] = self.get_reynolds(rho[i+1], u[i+1], self.Dh, mu[i+1])
                Pr[i+1] = self.get_prandtl(cp[i+1], mu[i+1], k[i+1])

                ff[i+1] = self.ff_cor.ff(Re[i+1], Pr[i+1])

                rho_avg = (rho[i] + rho[i+1])/2
                u_avg = (u[i] + u[i+1]) / 2
                ff_avg = (ff[i] + ff[i+1]) / 2

                C1 = P[i]
                C2 = rho[i]*u[i]**2
                C3 = -rho[i+1]*u[i+1]**2
                C4 = -(ff_avg*self.dx*rho_avg*u_avg**2)/(2*self.Dh)

                P_new = C1 + C2 + C3 + C4
                momentum_res = (P[i+1] - P_new)**2

                P[i+1] = P_new

                # Energy Equation
                Nu[i+1] = self.Nu_cor.Nu(Re[i+1], Pr[i+1])
                htc[i+1] = Nu[i+1] * k[i+1] / self.Dh

                htc_avg = (htc[i] + htc[i+1])/2
                T_avg = (T[i] + T[i+1])/2

                C1 = 1/(u[i+1]*rho[i+1])
                C2 = self.dx*htc_avg*self.P_wall*(T_wall[i]-T_avg)/self.A
                C3 = -u[i+1]*P[i+1]
                C4 = u[i]*rho[i]*E[i]
                C5 = u[i]*P[i]

                E_new = C1*(C2+C3+C4+C5)
                energy_res = (E[i+1] - E_new)**2

                E[i+1] = E_new
                e[i+1] = E[i+1] - 0.5*u[i+1]**2

                # Fluid Properties to get T and rho

                cv_avg = 0.5*cv[i+1] + 0.5*cv[i]
                T[i+1] = (e[i+1] - e[i])*cv_avg + T[i]

                rho_new = self.fluid.rho_from_T_P(T[i+1], P[i+1])
                rho_res = (rho[i+1 - rho_new])**2
                rho[i+1] = rho_new

                if(np.sqrt(mass_res + momentum_res + energy_res + rho_res) < self.tol):
                    break

        T0_out = T[-1] + (0.5*u[-1]**2)/cp[-1]
        P0_out = P[-1] + 0.5*rho[-1]*u[-1]**2

        # Update output variables
        self.outputs.T0_out.set(T0_out)
        self.outputs.P0_out.set(P0_out)
        self.outputs.m_dot.set(m_dot)

        self.outputs.T.set(T)
        self.outputs.P.set(P)
        self.outputs.rho.set(rho)
        self.outputs.u.set(u)
        self.outputs.e.set(e)
        self.outputs.E.set(E)

        self.outputs.mu.set(mu)
        self.outputs.cp.set(cp)
        self.outputs.k.set(k)

        self.outputs.Re.set(Re)
        self.outputs.Pr.set(Pr)

        self.outputs.ff.set(ff)
        self.outputs.Nu.set(Nu)
        self.outputs.htc.set(htc)