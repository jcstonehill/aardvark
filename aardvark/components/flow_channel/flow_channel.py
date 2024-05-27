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
            
            Q_dot : adv.FloatVar
                Total heat added to flow channel in [W]. Only used if hx_type =
                "use_Q_dot".

            Q_dot_shape : adv.Mesh1DVar
                Relative fraction of Q_dot added to each cell. This array is
                normalized internally so the sum of the array is equal to 1.
                Only used if hx_type = "use_Q_dot".

            T_wall : adv.Mesh1DVar
                Wall temperature in [K] used in heat transfer calculation. Only
                used if hx_type = "use_T_wall".
        """

        def __init__(self):
            self.inlet = adv.FlowStateVar("inlet", None)

            self.Q_dot = adv.FloatVar("Q_dot", 0)
            self.Q_dot_shape = adv.Mesh1DVar("Q_dot_shape", 1, "cell")

            self.T_wall = adv.Mesh1DVar("T_wall", 300, "cell")

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

            Q_dot : adv.FloatVar
                Total heat added to flow channel in [W]. 

            Q_dot_shape : adv.Mesh1DVar
                Relative fraction of Q_dot added to each cell. This array is
                normalized internally so the sum of the array is equal to 1.

            T_wall : adv.Mesh1DVar
                Wall temperature at each cell in [K]. Length is equal to number
                of cells (number of nodes - 1).
                Initialized to 300 [K].
        """

        def __init__(self):
            self.outlet = adv.FlowStateVar("outlet", (300, 101325, 0.001))

            self.T = adv.Mesh1DVar("T", 300, "node")
            self.P = adv.Mesh1DVar("P", 101325, "node")
            self.u = adv.Mesh1DVar("u", 1, "node")

            self.Q_dot = adv.FloatVar("Q_dot", 0)
            self.Q_dot_shape = adv.Mesh1DVar("Q_dot_shape", 1, "cell")
            self.T_wall = adv.Mesh1DVar("T_wall", 300, "cell")

    def __init__(self, name: str, mesh: adv.Mesh1D, A: float, P_wall: float,  
                 eps: float, fluid: adv.Fluid, hx_type: str = "adiabatic", Nu_func = adv.functions.dittus_boelter,
                 ff_func = adv.functions.churchill, tol: float = 1e-6, 
                 max_iter_per_node: float = 100):
        
        self.register(name)

        self.mesh: adv.Mesh1D = mesh
        self.A = adv.np.array(A)
        self.P_wall = adv.np.array(P_wall)
        self.eps = adv.np.array(eps)
        self.fluid = fluid
        self.hx_type = hx_type

        self.Nu_func = Nu_func
        self.ff_func = ff_func
        self.tol = adv.np.array(tol)
        self.max_iter_per_node = adv.np.array(max_iter_per_node)

        self.inputs = FlowChannel1D.Inputs()
        self.outputs = FlowChannel1D.Outputs()

    def setup(self):
        """ Setup all input and output variables. Mesh arrays are
            calculated and passed to mesh variables.

        """

        self.inputs.inlet.setup()

        if(self.hx_type == "use_T_wall"):
            self.inputs.T_wall.setup(self.mesh)

        elif(self.hx_type == "use_Q_dot"):
            self.inputs.Q_dot.setup()
            self.inputs.Q_dot_shape.setup(self.mesh)
        
        self.outputs.outlet.setup()
        
        self.outputs.T.setup(self.mesh)
        self.outputs.P.setup(self.mesh)
        self.outputs.u.setup(self.mesh)
        
        self.outputs.Q_dot.setup()
        self.outputs.Q_dot_shape.setup(self.mesh)
        self.outputs.T_wall.setup(self.mesh)

    def solve_steady_state(self):

        # Inputs
        T0_in, P0_in, m_dot = self.inputs.inlet.value

        if(self.hx_type == "adiabatic"):
            T_wall = adv.np.zeros(self.mesh.cells.size)
            Q_dot = 0
            Q_dot_shape = adv.np.ones(self.mesh.cells.size) / self.mesh.cells.size

        elif(self.hx_type == "use_Q_dot"):
            T_wall = adv.np.zeros(self.mesh.cells.size)
            Q_dot = self.inputs.Q_dot.value
            Q_dot_shape = self.inputs.Q_dot_shape.value / adv.np.sum(self.inputs.Q_dot_shape.value)

        elif(self.hx_type == "use_T_wall"):
            T_wall = self.inputs.T_wall.value
            Q_dot = 0
            Q_dot_shape = adv.np.zeros(self.mesh.cells.size)

        # Attributes
        A = self.A
        P_wall = self.P_wall
        eps = self.eps

        fluid = self.fluid
        Nu_func = self.Nu_func
        ff_func = self.ff_func
        tol = self.tol
        max_iter_per_node = self.max_iter_per_node

        # Initialize output arrays
        T = adv.np.zeros(self.mesh.nodes.size)      # Temperature                      [K]
        P = adv.np.zeros(self.mesh.nodes.size)      # Pressure                         [Pa]
        u = adv.np.zeros(self.mesh.nodes.size)      # Velocity                         [m/s]

        # Initialize post processing arrays
        rho = adv.np.zeros(self.mesh.nodes.size)    # Mass Density                     [kg/m^3]
        mu = adv.np.zeros(self.mesh.nodes.size)     # Dynamic Viscosity                [Pa-s]
        cp = adv.np.zeros(self.mesh.nodes.size)     # Specific Heat (Const P)          [J/kg-K]
        k = adv.np.zeros(self.mesh.nodes.size)      # Thermal Conductivity             [W/m-K]

        e = adv.np.zeros(self.mesh.nodes.size)      # Specific internal energy         [J/kg]
        E = adv.np.zeros(self.mesh.nodes.size)      # Total specific internal energy   [J/kg]

        Re = adv.np.zeros(self.mesh.nodes.size)     # Reynolds Number                  [Non-dimensional]
        Pr = adv.np.zeros(self.mesh.nodes.size)     # Prandtl Number                   [Non-dimensional]

        ff = adv.np.zeros(self.mesh.nodes.size)     # Friction Factor                  [Non-dimensional]
        Nu = adv.np.zeros(self.mesh.nodes.size)     # Nusselt Number                   [Non-dimensional]
        htc = adv.np.zeros(self.mesh.nodes.size)    # Heat Transfer Coefficient        [W/m^2-K]

        # Calculate geometry from inputs
        Dh = 4*A/P_wall             # Hydraulic Diameter            [m^2]

        # Get Static Conditions
        T_in, P_in = adv.functions.stagnation_to_static_flow(T0_in, P0_in, m_dot, A, fluid, 
                                                             max_iter_per_node, tol)

        print(T_in, P_in)

        # Add inlet values to variable arrays
        T[0] = T_in
        P[0] = P_in

        rho[0] = fluid.rho_from_T_P(T[0], P[0])
        mu[0] = fluid.mu_from_T_P(T[0], P[0])
        cp[0] = fluid.cp_from_T_P(T[0], P[0])
        k[0] = fluid.k_from_T_P(T[0], P[0])

        u[0] = m_dot / (rho[0]*A)
        e[0] = fluid.e_from_T_P(T[0], P[0])
        E[0] = e[0] + 0.5*u[0]**2

        Re[0] = adv.functions.reynolds(rho[0], u[0], Dh, mu[0])
        Pr[0] = adv.functions.prandtl(cp[0], mu[0], k[0])

        ff[0] = ff_func(eps, Dh, Re[0])
        Nu[0] = Nu_func(Re[0], Pr[0])
        
        htc[0] = Nu[0] * k[0] / Dh

        # MAIN SOLUTION LOOP
        for i in range(self.mesh.cells.size):
            # Set initial guess for next node
            T[i+1] = T[i]
            P[i+1] = P[i]

            rho[i+1] = rho[i]
            mu[i+1] = mu[i]
            cp[i+1] = cp[i]
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
            iter_no = 0
            while(True):

                iter_no += 1

            # Mass Conservation
                u_new = rho[i]*u[i]/rho[i+1]
                mass_res = (u[i+1] - u_new)**2

                u[i+1] = u_new

            # Momentum Conservation
                mu[i+1] = fluid.mu_from_T_P(T[i+1], P[i+1])
                cp[i+1] = fluid.cp_from_T_P(T[i+1], P[i+1])
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
                C4 = -(ff_avg*self.mesh.dx[i]*rho_avg*u_avg**2)/(2*Dh)

                P_new = C1 + C2 + C3 + C4

                momentum_res = (P[i+1] - P_new)**2

                P[i+1] = P_new
                
            # Energy Equation
                Nu[i+1] = Nu_func(Re[i+1], Pr[i+1])
                
                htc[i+1] = Nu[i+1] * k[i+1] / Dh

                htc_avg = (htc[i] + htc[i+1])/2
                T_avg = (T[i] + T[i+1])/2

                if(self.hx_type == "adiabatic"):
                    T_wall[i] = T_avg

                elif(self.hx_type == "use_T_wall"):
                    local_Q_dot = self.mesh.dx[i]*htc_avg*self.P_wall*(T_wall[i] - T_avg)/self.A
                    Q_dot += local_Q_dot
                    Q_dot_shape[i] = local_Q_dot

                elif(self.hx_type == "use_Q_dot"):
                    T_wall[i] = Q_dot*Q_dot_shape[i]*A/(htc_avg*P_wall*self.mesh.dx[i]) + T_avg

                # C1 through C5 are just intermediate values to calculate
                # energy equation.
                C1 = 1/(u[i+1]*rho[i+1])
                C2 = Q_dot*Q_dot_shape[i]
                C3 = -u[i+1]*P[i+1]
                C4 = u[i]*rho[i]*E[i]
                C5 = u[i]*P[i]

                E_new = C1*(C2+C3+C4+C5)
                energy_res = (E[i+1] - E_new)**2

                E[i+1] = E_new
                e[i+1] = E[i+1] - 0.5*u[i+1]**2

                # Use equation of state to get temperature.
                T[i+1] = fluid.T_from_e_P(e[i+1], P[i+1])

            # Mass density from fluid properties calculation.
                rho_new = fluid.rho_from_T_P(T[i+1], P[i+1])
                rho_res = (rho[i+1] - rho_new)**2
                rho[i+1] = rho_new

            # Check residual to see if this node has converged.
                if(adv.np.max(adv.np.sqrt([mass_res, momentum_res, energy_res, rho_res])) < tol):
                    break

                if(iter_no > max_iter_per_node):
                    self.log_error("Node did not converge after " + str(max_iter_per_node) + " iterations.")
 
        T0_out, P0_out = adv.functions.static_to_stagnation_flow(T[-1], P[-1], m_dot, A, fluid)

        # Update outputs
        self.outputs.outlet.value = (T0_out, P0_out, m_dot)

        self.outputs.T.value = T
        self.outputs.P.value = P
        self.outputs.u.value = u

        self.outputs.Q_dot.value = Q_dot
        self.outputs.Q_dot_shape.value = Q_dot_shape
        self.outputs.T_wall.value = T_wall
        
        

        # TODO Post values as well.