import aardvark.internal_api as adv

import numpy as np

class FlowChannel1DInputs(adv.DataSet):
    def __init__(self):
        self.T0_in: adv.FloatVar = None
        self.P0_in: adv.FloatVar = None
        self.m_dot: adv.FloatVar = None

        self.T_wall: adv.FloatArrayVar = None
        self.Q_dot: adv.FloatArrayVar = None

class FlowChannel1DOutputs(adv.DataSet):
    def __init__(self):
        self.T0_out: adv.FloatVar = adv.System.define_variable(adv.FloatVar)
        self.P0_out: adv.FloatVar = adv.System.define_variable(adv.FloatVar)
        self.m_dot: adv.FloatVar = adv.System.define_variable(adv.FloatVar)

        self.node_x: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

        self.T: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.P: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.u: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.e: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.E: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

        self.rho: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.mu: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.cp: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.cv: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.k: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

        self.Re: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.Pr: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

        self.ff: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.Nu: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.htc: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

        self.T_wall: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)
        self.Q_dot: adv.FloatArrayVar = adv.System.define_variable(adv.FloatArrayVar)

class FlowChannel1DInitialConditions(adv.DataSet):
    def __init__(self):
        self.T0_out = 300
        self.P0_out = 101325
        self.m_dot = 0.001
        
        self.node_x = np.array([0, 1])

        self.T = 300
        self.P = 300
        self.u = 1
        self.e = 0
        self.E = 0

        self.rho = 0.1
        self.mu = 1e-5
        self.cp = 5000
        self.cv = 3000
        self.k = 0.1

        self.Re = 220
        self.Pr = 0.5

        self.ff = 0.2909
        self.Nu = 1
        self.htc = 1.5

        self.T_wall = 300
        self.Q_dot = 0

class FlowChannel1D(adv.Component):

    # https://cardinal.cels.anl.gov/theory/thm.html

    component_name = "FlowChannel1D"

    def __init__(self, name: str, N: float, A: float, P_wall: float, L: float, eps: float, 
                 fluid: adv.Fluid, Nu_func: function = adv.functions.dittus_boelter,
                 ff_func: function = adv.functions.churchill, tol: float = 1e-6, 
                 max_iter_per_node: float = 100):
        self.name = name
        self.N = N
        self.A = A
        self.P_wall = P_wall
        self.L = L
        self.eps = eps
        self.fluid = fluid
        self.Nu_func = Nu_func
        self.ff_func = ff_func
        self.tol = tol
        self.max_iter_per_node = max_iter_per_node

        self.inputs = FlowChannel1DInputs()
        self.outputs = FlowChannel1DOutputs()
        self.initial = FlowChannel1DInitialConditions()

    def solve_steady_state(self):
        # Inputs
        T0_in = self.inputs.T0_in.get()
        P0_in = self.inputs.P0_in.get()
        m_dot = self.inputs.m_dot.get()

        T_wall = self.inputs.T_wall.get()
        Q_dot = self.inputs.Q_dot.get()

        # Setup
        N = self.N
        A = self.A
        P_wall = self.P_wall
        L = self.L
        eps = self.eps

        fluid = self.fluid
        Nu_func = self.Nu_func
        ff_func = self.ff_func
        tol = self.tol
        max_iter_per_node = self.max_iter_per_node

        # Outputs
        T = np.zeros(N+1)
        P = np.zeros(N+1)

        rho = np.zeros(N+1)
        mu = np.zeros(N+1)
        cp = np.zeros(N+1)
        cv = np.zeros(N+1)
        k = np.zeros(N+1)

        u = np.zeros(N+1)
        e = np.zeros(N+1)
        E = np.zeros(N+1)

        Re = np.zeros(N+1)
        Pr = np.zeros(N+1)

        ff = np.zeros(N+1)
        Nu = np.zeros(N+1)
        htc = np.zeros(N+1)

        # Determine heat transfer BC
        if(T_wall is not None and Q_dot is not None):
            #TODO update this using logger
            raise Exception("Both T_wall and Q_dot can't be prescribed.")

        if(T_wall is not None):
            hx_type = "use_T_wall"
            Q_dot = np.zeros(N)

        elif(Q_dot is not None):
            hx_type = "use_Q_dot"
            T_wall = np.zeros(N)

        else:
            hx_type = "adiabatic"
            Q_dot = np.zeros(N)
            T_wall = np.zeros(N)
        

        # Calculate geometry from inputs
        Dh = 4*A/P_wall
        dx = L/N

        # Get Static Conditions
        T_in, P_in = adv.functions.stagnation_to_static_flow(T0_in, P0_in, m_dot, A, fluid, 
                                                             max_iter_per_node, tol)

        # Add inlet values to variable arrays
        T[0] = T_in
        P[0] = P_in

        rho[0] = fluid.rho_from_T_P(T[0], P[0])
        mu[0] = fluid.mu_from_T_P(T[0], P[0])
        cp[0] = fluid.cp_from_T_P(T[0], P[0])
        cv[0] = fluid.cv_from_T_P(T[0], P[0])
        k[0] = fluid.k_from_T_P(T[0], P[0])

        u[0] = m_dot / (rho[0]*A)
        e[0] = cv[0]*T[0]
        E[0] = e[0] + 0.5*u[0]**2

        Re[0] = adv.functions.reynolds(rho[0], u[0], Dh, mu[0])
        Pr[0] = adv.functions.prandtl(cp[0], mu[0], k[0])

        ff[0] = ff_func(eps, Dh, Re[0])
        Nu[0] = Nu_func(Re[0], Pr[0])
        
        htc[0] = Nu[0] * k[0] / Dh

        # MAIN LOOP
        for i in range(N):
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
            for _ in range(max_iter_per_node):
                # Mass Conservation
                u_new = rho[i]*u[i]/rho[i+1]
                mass_res = (u[i+1] - u_new)**2

                u[i+1] = u_new

                # Momentum Conservation
                mu[i+1] = fluid.mu_from_T_P(T[i+1], P[i+1])
                cp[i+1] = fluid.cp_from_T_P(T[i+1], P[i+1])
                cv[i+1] = fluid.cv_from_T_P(T[i+1], P[i+1])
                k[i+1] = fluid.k_from_T_P(T[i+1], P[i+1])

                Re[i+1] = adv.functions.reynolds(rho[i+1], u[i+1], Dh, mu[i+1])
                Pr[i+1] = adv.functions.prandtl(cp[i+1], mu[i+1], k[i+1])
                
                ff[i+1] = ff_func(eps, Dh, Re[i+1])
                
                rho_avg = (rho[i] + rho[i+1])/2
                u_avg = (u[i] + u[i+1]) / 2
                ff_avg = (ff[i] + ff[i+1]) / 2

                C1 = P[i]
                C2 = rho[i]*u[i]**2
                C3 = -rho[i+1]*u[i+1]**2
                C4 = -(ff_avg*dx*rho_avg*u_avg**2)/(2*Dh)

                P_new = C1 + C2 + C3 + C4

                momentum_res = (P[i+1] - P_new)**2

                P[i+1] = P_new

                # Energy Equation
                Nu[i+1] = Nu_func(Re[i+1], Pr[i+1])
                
                htc[i+1] = Nu[i+1] * k[i+1] / Dh

                htc_avg = (htc[i] + htc[i+1])/2
                T_avg = (T[i] + T[i+1])/2

                C1 = 1/(u[i+1]*rho[i+1])

                if(hx_type == "adiabatic"):
                    C2 = 0

                elif(hx_type == "use_T_wall"):
                    C2 = dx*htc_avg*P_wall*(T_wall[i]-T_avg)/A
                    Q_dot[i] = C2

                elif(hx_type == "use_Q_dot"):
                    C2 = Q_dot[i]
                    T_wall[i] = Q_dot[i]*A/(dx*htc_avg*P_wall) + T_avg

                else:
                    raise Exception("Unknown hx_type")

                C3 = -u[i+1]*P[i+1]
                C4 = u[i]*rho[i]*E[i]
                C5 = u[i]*P[i]

                E_new = C1*(C2+C3+C4+C5)
                energy_res = (E[i+1] - E_new)**2

                E[i+1] = E_new
                e[i+1] = E[i+1] - 0.5*u[i+1]**2

                # Fluid Properties to get T and rho

                cv_avg = 0.5*cv[i+1] + 0.5*cv[i]
                T[i+1] = (e[i+1] - e[i])/cv_avg + T[i]

                rho_new = fluid.rho_from_T_P(T[i+1], P[i+1])
                rho_res = (rho[i+1] - rho_new)**2
                rho[i+1] = rho_new

                if(np.sqrt(mass_res + momentum_res + energy_res + rho_res) < tol):
                    break

        T0_out, P0_out = adv.functions.static_to_stagnation_flow(T[-1], P[-1], m_dot, A, fluid)

        # Update output variables
        self.outputs.T0_out.set(T0_out)
        self.outputs.P0_out.set(P0_out)
        self.outputs.m_dot.set(m_dot)

        self.outputs.node_x.set(np.linspace(0, L, N+1))

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
        
        self.outputs.T_wall.set(T_wall)
        self.outputs.Q_dot.set(Q_dot)