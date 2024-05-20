import aardvark.internal_api as adv

from decimal import Decimal

import numpy as np



def solve_components():
    for component in adv.components:
        component.solve_steady_state()

def residual() -> float:
    res = 0

    for variable in adv.variables:
        res += variable.r2()

    res = np.sqrt(res)

    return res

def solve_steady_state(case_name: str, tol = 1e-6, max_iter = 1000):
    adv.create_outputs_dir(case_name)

    adv.Log.message("Steady state solver is starting.")

    # Initial Iteration
    solve_components()

    res = residual()

    adv.Log.line_break()
    adv.Log.message("     %-9s     %-12s" % ("Iteration", "Residual"))
    adv.Log.message("     %-9s     %-12E" % ("Initial", Decimal(res)))

    for i in range(10):
        adv.Log.message("     %-9i     %-12E" % (10 ** (i/2), Decimal(20 ** (i/2))))



    