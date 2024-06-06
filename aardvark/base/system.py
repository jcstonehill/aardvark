from aardvark.base.component import Component
from aardvark.base.variables import Variable
from aardvark.base.log import Log

import os
from decimal import Decimal


class System:
    @classmethod
    def create_outputs_dir(cls, desired_case_name: str):
        outputs_dir_exists = os.path.isdir("output")

        if(not outputs_dir_exists):
            os.mkdir("output")

        case_exists = os.path.isdir("output/" + desired_case_name)

        if(case_exists):
            case_name = cls.modify_case_name(desired_case_name)

        else:
            case_name = desired_case_name

        os.mkdir("output/" + case_name)
        
        Log.create(case_name)

        if(not outputs_dir_exists):
            Log.message("Output folder not found. Created new outputs folder.")

        if(case_exists):
            Log.message("A case named \"" + desired_case_name + "\" already exists. Modifying case name to \"" + case_name + "\".")
            
        Log.message("Created case named \"" + str(case_name) + "\".")

    @classmethod
    def modify_case_name(cls, orig_case_name: str) -> str:
        i = 0

        new_case_name = orig_case_name

        while(os.path.isdir("output/" + new_case_name)):
            i += 1
            new_case_name = orig_case_name + "-" + str(i)

        return new_case_name
    
    def __init__(self):
        self._components: list[Component] = []

    def add_component(self, component: Component):
        self._components.append(component)

    def solve_components(self, dt: float):
        for component in self._components:
            component.solve(dt)

    def solve(self, dt: float, tol: float, max_iter: float):

        self.solve_components(dt)
        res = self.residual()

        Log.line_break()
        Log.message("     %-9s     %-12s" % ("Iteration", "Residual"))
        Log.message("     %-9s     %-12E" % ("Initial", Decimal(res)))

        i = 0

        while(True):
            if(i >= max_iter):
                Log.message("Max iterations reached without convergence.")
                break

            self.solve_components(dt)
            res = self.residual()

            Log.message("     %-9i     %-12E" % (i, Decimal(res)))

            if(res <= tol):
                Log.message("Time step converged in " + str(i) + " iterations.")
                break

            i += 1
            
    def setup(self):
        for component in self._components:
            component.setup()

            Log.message("Component \"" + component._name + "\" was setup.")

    def residual(self) -> float:
        res = 0

        for component in self._components:
            res += component.residual()

        return res