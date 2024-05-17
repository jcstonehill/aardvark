import aardvark.internal_api as adv

class ConstantFluid(adv.FluidBase):
    
    def __init__(self, rho: float, cp: float, cv: float, mu: float, k: float):
        self.rho = rho
        self.cp = cp
        self.cv = cv
        self.mu = mu
        self.k = k

    def rho_from_T_P(self, T: float, P: float) -> float:
        return self.rho

    def cp_from_T_P(self, T: float, P: float) -> float:
        return self.cp

    def cv_from_T_P(self, T: float, P: float) -> float:
        return self.cv

    def mu_from_T_P(self, T: float, P: float) -> float:
        return self.mu

    def k_from_T_P(self, T: float, P: float) -> float:
        return self.k