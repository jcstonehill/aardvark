import aardvark.internal_api as adv


class FlowChannel1D(adv.Component):
    """ Solves the 1D area averaged Navier-Stokes equations for internal flow.

    Parameters
    ----------
    name : str
        Unique name to identify the component.

    node_x : Iterable of Float
        x locations of the nodes in [m]. Most flow variables (temperature,
        pressure, velocity, etc) are solved at each of these locations.

    A : float
        Cross sectional flow area of the channel in [m^2]

    P_wall : float
        Wetted perimeter of the channel in [m^2].

    eps : float
        Wall roughness [m].

    fluid : adv.Fluid
        Material object representing the fluid properties in the channel.

    Nu_func : function
        Function used to calculate Nusselt number.

    ff_func : function
        Function used to calculate friction factor.

    tol : float
        Tolerance for residuals of Navier-Stokes equations at each node.

    max_iter_per_node : int
        Maximum number of non-linear iterations per node.
    
    """

    component_name = "FlowChannel1D"

    class Inputs:
        """ Inputs for FlowChannel1D Component.

            Attributes
            ----------
            inlet : adv.FlowStateVar
                Flow state at inlet (T0 [K], P0 [Pa], m_dot [kg/s])
            
            Q_dot : adv.Mesh1DVar
                Heat addition at each cell in [W]. Length is equal to number of
                cells (number of nodes - 1).
        """
        def __init__(self):
            self.inlet = adv.FlowStateVar("inlet", None, None, None)

            self.Q_dot = adv.Mesh1DVar("Q_dot", 0)

    class Outputs:
        """ Outputs for FlowChannel1D Component.

            Attributes
            ----------
            outlet : adv.FlowStateVar
                Flow state at outlet (T0 [K], P0 [Pa], m_dot [kg/s]).
                Initialized to (300, 101325, 0.001).
            
            T : adv.Mesh1DVar
                Static temperature at each node in [K]. Length is equal to
                number of nodes.
                Initialized to 300 [K].

            P : adv.Mesh1DVar
                Static pressure at each node in [Pa]. Length is equal to number
                of nodes.
                Initialized to 101325 [Pa].

            u : adv.Mesh1DVar
                Flow velocity at each node in [m/s]. Length is equal to number
                of nodes.
                Initialized to 1 [m/s].

            T_wall : adv.Mesh1DVar
                Wall temperature at each cell in [K]. Length is equal to number
                of cells (number of nodes - 1).
                Initialized to 300 [K].
        """

        def __init__(self):
            self.outlet = adv.FlowStateVar("outlet", 300, 101325, 0.001)

            self.T = adv.Mesh1DVar("T", 300)
            self.P = adv.Mesh1DVar("P", 101325)
            self.u = adv.Mesh1DVar("u", 1)

            self.T_wall = adv.Mesh1DVar("T_wall", 300)

    def __init__(self, name: str, node_x: adv.np.ndarray, A: float, P_wall: float,  
                 eps: float, fluid: adv.Fluid, Nu_func = adv.functions.dittus_boelter,
                 ff_func = adv.functions.churchill, tol: float = 1e-6, 
                 max_iter_per_node: float = 100):
        
        self.register(name)

        self.node_x = node_x
        self.A = A
        self.P_wall = P_wall
        self.eps = eps
        self.fluid = fluid
        self.Nu_func = Nu_func
        self.ff_func = ff_func
        self.tol = tol
        self.max_iter_per_node = max_iter_per_node

        self.N = len(node_x) - 1
        
        self.inputs = FlowChannel1D.Inputs()
        self.outputs = FlowChannel1D.Outputs()

    def initialize(self):
        """ Initialize all input and output variables. Mesh arrays are
            calculated and passed to mesh variables.

        """

        self.cell_x = [(0.5*self.node_x[i+1] + 0.5*self.node_x[i]) for i in range(self.N)]

        self.inputs.inlet.initialize()
        self.inputs.Q_dot.initialize(self.cell_x)

        self.outputs.outlet.initialize()
        
        self.outputs.T.initialize(self.node_x)
        self.outputs.P.initialize(self.node_x)
        self.outputs.u.initialize(self.node_x)
        
        self.outputs.T_wall.initialize(self.cell_x)

    def solve_steady_state(self):

        # Inputs
        T0_in = self.inputs.inlet.T0
        P0_in = self.inputs.inlet.P0
        m_dot = self.inputs.inlet.m_dot

        Q_dot = self.inputs.Q_dot.value

        # Attributes
        N = self.N
        A = self.A
        P_wall = self.P_wall
        eps = self.eps

        fluid = self.fluid
        Nu_func = self.Nu_func
        ff_func = self.ff_func
        tol = self.tol
        max_iter_per_node = self.max_iter_per_node

        # Initialize output arrays
        T = adv.np.zeros(N+1)       # Temperature                   [K]
        P = adv.np.zeros(N+1)       # Pressure                      [Pa]
        u = adv.np.zeros(N+1)       # Velocity                      [m/s]

        T_wall = adv.np.zeros(N)    # Wall Temperature              [K]

        # Initialize post processing arrays
        rho = adv.np.zeros(N+1)     # Mass Density                  [kg/m^3]
        mu = adv.np.zeros(N+1)      # Dynamic Viscosity             [Pa-s]
        cp = adv.np.zeros(N+1)      # Specific Heat (Const P)       [J/kg-K]
        cv = adv.np.zeros(N+1)      # Specific Heat (Const V)       [J/kg-K]
        k = adv.np.zeros(N+1)       # Thermal Conductivity          [W/m-K]
        
        e = adv.np.zeros(N+1)       # Specific internal energy      [J/kg]
        E = adv.np.zeros(N+1)       # Total specific internal energy[J/kg]

        Re = adv.np.zeros(N+1)      # Reynolds Number               [Non-dimensional]
        Pr = adv.np.zeros(N+1)      # Prandtl Number                [Non-dimensional]

        ff = adv.np.zeros(N+1)      # Friction Factor               [Non-dimensional]
        Nu = adv.np.zeros(N+1)      # Nusselt Number                [Non-dimensional]
        htc = adv.np.zeros(N+1)     # Heat Transfer Coefficient     [W/m^2-K]

        # Calculate geometry from inputs
        Dh = 4*A/P_wall             # Hydraulic Diameter            [m^2]
        dx = adv.np.array([self.node_x[i+1] - self.node_x[i] for i in range(self.N)])   # Length of each cell

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

        # MAIN SOLUTION LOOP
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

                # C1 through C4 are just intermediate values to calculate
                # momentum equation.
                C1 = P[i]
                C2 = rho[i]*u[i]**2
                C3 = -rho[i+1]*u[i+1]**2
                C4 = -(ff_avg*dx[i]*rho_avg*u_avg**2)/(2*Dh)

                P_new = C1 + C2 + C3 + C4

                momentum_res = (P[i+1] - P_new)**2

                P[i+1] = P_new

            # Energy Equation
                Nu[i+1] = Nu_func(Re[i+1], Pr[i+1])
                
                htc[i+1] = Nu[i+1] * k[i+1] / Dh

                htc_avg = (htc[i] + htc[i+1])/2
                T_avg = (T[i] + T[i+1])/2

                # C1 through C5 are just intermediate values to calculate
                # energy equation.
                C1 = 1/(u[i+1]*rho[i+1])
                C2 = Q_dot[i]
                C3 = -u[i+1]*P[i+1]
                C4 = u[i]*rho[i]*E[i]
                C5 = u[i]*P[i]

                E_new = C1*(C2+C3+C4+C5)
                energy_res = (E[i+1] - E_new)**2

                # Back calculate temperature from internal energy.
                E[i+1] = E_new
                e[i+1] = E[i+1] - 0.5*u[i+1]**2

                cv_avg = 0.5*cv[i+1] + 0.5*cv[i]
                T[i+1] = (e[i+1] - e[i])/cv_avg + T[i]

            # Mass density from fluid properties calculation.
                rho_new = fluid.rho_from_T_P(T[i+1], P[i+1])
                rho_res = (rho[i+1] - rho_new)**2
                rho[i+1] = rho_new

            # Check residual to see if this node has converged.
                if(adv.np.sqrt(mass_res + momentum_res + energy_res + rho_res) < tol):
                    break

            # Node has converged, so wall temperature can now be calculated.
            T_wall[i] = Q_dot[i]*A/(dx[i]*htc_avg*P_wall) + T_avg

        T0_out, P0_out = adv.functions.static_to_stagnation_flow(T[-1], P[-1], m_dot, A, fluid)

        # Update outputs
        self.outputs.outlet.T0 = T0_out
        self.outputs.outlet.P0 = P0_out
        self.outputs.outlet.m_dot = m_dot

        self.outputs.T.value = T
        self.outputs.P.value = P
        self.outputs.u.value = u

        self.outputs.T_wall.value = T_wall

        # TODO Post values as well.