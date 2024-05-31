from aardvark.base.fluid import Fluid

from CoolProp.CoolProp import PropsSI


class Hydrogen(Fluid):

    fluid_name = "Hydrogen"

    def rho_from_T_P(self, T: float, P: float) -> float:
        return PropsSI("D", "T", T, "P", P, self.fluid_name)
    
    def cp_from_T_P(self, T: float, P: float) -> float:
        print(T, P)
        return PropsSI("C", "T", T, "P", P, self.fluid_name)

    def mu_from_T_P(self, T: float, P: float) -> float:
        print(T, P)
        return PropsSI("V", "T", T, "P", P, self.fluid_name)

    def k_from_T_P(self, T: float, P: float) -> float:
        print(T, P)
        return PropsSI("L", "T", T, "P", P, self.fluid_name)

    def e_from_T_P(self, T: float, P: float) -> float:
        print(T, P)
        return PropsSI("U", "T", T, "P", P, self.fluid_name)

    def T_from_e_P(self, e: float, P: float) -> float:
        # if(e>15695007):
        #     e_prop = 15695007
        # else:
        #     e_prop = e
        return PropsSI("T", "U", e, "P", P, self.fluid_name)
    
    def T_max(self):
        return PropsSI("TMAX", self.fluid_name)