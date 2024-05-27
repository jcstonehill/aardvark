# import aardvark.internal_api as adv

# class ConstantFluid(adv.Fluid):
    
#     def __init__(self, rho: float = 997, cp: float = 4184, cv: float = 4184, mu: float = 0.001, k: float = 0.6):
#         # Defaults are water properties

#         self.rho = rho
#         self.cp = cp
#         self.cv = cv
#         self.mu = mu
#         self.k = k

#     def rho_from_T_P(self, T: float, P: float) -> float:
#         return self.rho

#     def cp_from_T_P(self, T: float, P: float) -> float:
#         return self.cp

#     def h_from_T_P(self, T: float, P: float) -> float:
#         return self.cv

#     def mu_from_T_P(self, T: float, P: float) -> float:
#         return self.mu

#     def k_from_T_P(self, T: float, P: float) -> float:
#         return self.k