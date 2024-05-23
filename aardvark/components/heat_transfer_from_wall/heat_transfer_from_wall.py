import aardvark.internal_api as adv

class HeatTransferFromWall(adv.Component):
    class Inputs:
        """ Inputs for HeatTransferWall Component.

            Attributes
            ----------
            T_flow : adv.Mesh1DVar
                Static temperature of the flow in [K].
            
            T_wall : adv.Mesh1DVar
                Wall temperature in [K].

        """
        def __init__(self):
            self.T_flow = adv.Mesh1DVar("T_flow", None)
            self.T_wall = adv.Mesh1DVar("T_wall", None)
            self.htc = adv.Mesh1DVar("htc", None)

    class Outputs:
        """ Outputs for HeatTransferWall Component.

            Attributes
            ----------
            Q_dot : adv.Mesh1DVar
                Heat deposition to the flow in [W].

        """

        def __init__(self):
            self.Q_dot = adv.Mesh1DVar("Q_dot", 0)

    def __init__(self, name: str, node_x: adv.np.ndarray, P_wall: float):
        self.register(name)

        self.node_x = node_x
        self.P_wall = P_wall

        self.N = len(node_x) - 1

        self.inputs = HeatTransferFromWall.Inputs()
        self.outputs = HeatTransferFromWall.Outputs()

    def initialize(self):
        self.cell_x = [0.5*self.node_x[i+1] + 0.5*self.node_x[i] for i in range(self.N)]

        self.inputs.T_flow.initialize(self.node_x)
        self.inputs.T_wall.initialize(self.cell_x)
        self.inputs.htc.initialize(self.node_x)
        
        self.outputs.Q_dot.initialize(self.cell_x)

    def solve_steady_state(self):
        T_flow = self.inputs.T_flow.value
        T_wall = self.inputs.T_wall.value
        htc = self.inputs.htc.value

        Q_dot = adv.np.zeros(self.N)

        dx = [self.node_x[i+1] - self.node_x[i] for i in range(self.N)]

        for i in range(self.N):
            T_flow_avg = 0.5*T_flow[i+1] + 0.5*T_flow[i]

            htc_avg = 0.5*htc[i+1] + 0.5*htc[i]

            Q_dot[i] = htc_avg*(T_wall[i] - T_flow_avg)*self.P_wall*dx[i]

        self.outputs.Q_dot.value = Q_dot


        