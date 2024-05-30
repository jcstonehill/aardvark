from aardvark.base.fluid import Fluid

from CoolProp.CoolProp import PropsSI


class IdealGas(Fluid):

    fluid_name = ""

    def __init__(self, name: str, cp: float, k: float, molar_mass: float, mu: float):
        self.fluid_name = name

        self.cp = cp
        self.k = k
        self.molar_mass = molar_mass
        self.mu = mu

        self.R = 8314.46261815324 / molar_mass
        self.cv = self.cp - self.R

    def rho_from_T_P(self, T: float, P: float) -> float:
        return P/(self.R*T)
    
    def cp_from_T_P(self, T: float, P: float) -> float:
        return self.cp

    def mu_from_T_P(self, T: float, P: float) -> float:
        return self.mu

    def k_from_T_P(self, T: float, P: float) -> float:
        return self.k

    def e_from_T_P(self, T: float, P: float) -> float:
        return self.cv*T

    def T_from_e_P(self, e: float, P: float) -> float:
        return e/self.cv