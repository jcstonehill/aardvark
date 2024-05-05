import aardvark as adv

class FlowChannel1D(adv.ComponentBase):

# https://cardinal.cels.anl.gov/theory/thm.html

    inputs = {
        "T0_in"     :   300,
        "P0_in"     :   101325,
        "m_dot"     :   0.0008,
        "T_wall_z"  :   [0, 1],
        "T_wall"    :   [300]
    }

    outputs = {
        "Q_dot_z"   :   [0, 1],
        "Q_dot"     :   [0]
    }

    ic = {
        
    }

    def __init__(self, N: int, A: float,  L: float, fluid: adv.FluidBase, 
            nu_cor: adv.NuCorrelationBase, ff_cor: adv.FFCorrelationBase):
        """TODO fill this out.
        """
        self.N = N
        self.A = A
        self.L = L
        self.fluid = fluid
        self.nu_cor = nu_cor
        self.ff_cor = ff_cor

    def solve(self, dt: int):
        """TODO fill this out.
        """
        
        T0_in = self.inputs["T0_in"]
        P0_in = self.inputs["P0_in"]
        m_dot = self.inputs["m_dot"]
        T_wall_z = self.inputs["T_wall_z"]
        T_wall = self.inputs["T_wall"]

        