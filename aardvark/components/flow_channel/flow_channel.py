import aardvark.component_api as adv


class FlowChannel1D(adv.Component):
    componet_type = "FlowChannel1D"

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

        pass

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

        pass

    def __init__(self, name: str, mesh: adv.Mesh1D, A: float, P_wall: float,  
                 eps: float, fluid: adv.Fluid, hx_type: str = "adiabatic", tol: float = 1e-6, 
                 max_iter_per_node: float = 1000):
        self.initialize(name)

        self.mesh: adv.Mesh1D = mesh

        self.A = adv.np.array(A)
        self.P_wall = adv.np.array(P_wall)
        self.eps = adv.np.array(eps)

        self.fluid = fluid
        self.hx_type = hx_type

        self.tol = adv.np.array(tol)
        self.max_iter_per_node = adv.np.array(max_iter_per_node)

    def declare_variables(self):
        self.inlet = self.add_flow_state_var("inlet", "SI")
        self.outlet = self.add_flow_state_var("outlet", "SI")

        self.T = self.add_mesh1d_var("T", "K", "node")
        self.P = self.add_mesh1d_var("P", "Pa", "node")

        self.Q_dot = self.add_float_var("Q_dot", "W")
        self.Q_dot_shape = self.add_mesh1d_var("Q_dot_shape", "Unitless", "cell")
        self.T_wall = self.add_mesh1d_var("T_wall", "K", "cell")

    def setup(self):
        pass

    def solve(self, dt: float):

        # Inputs
        print(self.inlet.value)
        T0_in, P0_in, m_dot = self.inlet.value

        if(self.hx_type == "adiabatic"):
            T_wall = adv.np.zeros(self.mesh.cells.size)
            Q_dot = 0
            Q_dot_shape = adv.np.ones(self.mesh.cells.size) / self.mesh.cells.size

        elif(self.hx_type == "use_Q_dot"):
            T_wall = adv.np.zeros(self.mesh.cells.size)
            Q_dot = self.Q_dot.value
            Q_dot_shape = self.Q_dot_shape.value / adv.np.sum(self.Q_dot_shape.value)

        elif(self.hx_type == "use_T_wall"):
            T_wall = self.T_wall.value
            Q_dot = 0
            Q_dot_shape = adv.np.zeros(self.mesh.cells.size)

        # Attributes
        A = self.A
        P_wall = self.P_wall
        eps = self.eps

        fluid = self.fluid
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

        ff[0] = adv.functions.churchill(eps, Dh, Re[0])
        Nu[0] = adv.functions.dittus_boelter(Re[0], Pr[0])
        
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

            # Energy Equation
                Nu[i+1] = adv.functions.dittus_boelter(Re[i+1], Pr[i+1])
                
                htc[i+1] = Nu[i+1] * k[i+1] / Dh

                htc_avg = (htc[i] + htc[i+1])/2
                T_avg = (T[i] + T[i+1])/2

                if(self.hx_type == "adiabatic"):
                    T_wall[i] = T_avg

                elif(self.hx_type == "use_T_wall"):
                    local_Q_dot = htc_avg*self.mesh.dx[i]*self.P_wall*(T_wall[i] - T_avg)
                    Q_dot += local_Q_dot
                    Q_dot_shape[i] = local_Q_dot

                elif(self.hx_type == "use_Q_dot"):
                    local_Q_dot = Q_dot*Q_dot_shape[i]
                    T_wall[i] = Q_dot*Q_dot_shape[i]/(htc_avg*self.mesh.dx[i]*P_wall) + T_avg

                # C1 through C5 are just intermediate values to calculate
                # energy equation.
                C1 = 1/(u[i+1]*rho[i+1])
                C2 = local_Q_dot/A
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
                
                ff[i+1] = adv.functions.churchill(eps, Dh, Re[i+1])
                
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

            # Check residual to see if this node has converged.
                if(adv.np.max(adv.np.sqrt([mass_res, momentum_res, energy_res, rho_res])) < tol):
                    break

                if(iter_no > max_iter_per_node):
                    self.log_error("Node " + str(i) + " did not converge after " + str(max_iter_per_node) + " iterations.")
        
        T0_out, P0_out = adv.functions.static_to_stagnation_flow(T[-1], P[-1], m_dot, A, fluid)

        # Update outputs
        self.outlet.value = (T0_out, P0_out, m_dot)

        self.T.value = T
        self.P.value = P

        self.Q_dot.value = Q_dot
        self.Q_dot_shape.value = Q_dot_shape
        self.T_wall.value = T_wall
        
        

        # TODO Post values as well.