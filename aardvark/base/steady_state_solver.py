import aardvark.internal_api as adv

from decimal import Decimal
import time

def convert_computation_time(seconds, granularity = 5):
    if(seconds < 1):
        return "%-5f seconds" % (seconds)

    intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)
    
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def solve_components():
    for component in adv.components:
        component.solve_steady_state()

def residual() -> float:
    res = 0

    for component in adv.components:
        res += component.residual()

    return res

def setup_components():
    for component in adv.components:
        component.check_inputs()
        component.setup()
        adv.Log.message("Component \"" + component._name + "\" was initialized.")

def solve_steady_state(case_name: str, tol = 1e-6, max_iter = 1000):
    adv.System.create_outputs_dir(case_name)

    adv.Log.message("Setting up components...")
    setup_components()

    adv.Log.message("Starting steady state solution loop.")

    # Initial Iteration
    solve_components()

    res = residual()

    adv.Log.line_break()
    adv.Log.message("     %-9s     %-12s" % ("Iteration", "Residual"))
    adv.Log.message("     %-9s     %-12E" % ("Initial", Decimal(res)))

    start_time = time.time()

    i = 0
    while(True):
        i += 1

        solve_components()
        res = residual()

        adv.Log.message("     %-9i     %-12E" % (i, Decimal(res)))

        if(res <= tol):
            adv.Log.message("Converged in " + str(i) + " iterations.")
            break

        if(i >= max_iter):
            adv.Log.message("Max iterations reached without convergence.")
            break

    adv.Log.line_break()

    end_time = time.time()

    adv.Log.message("Computation Time was " + convert_computation_time(end_time-start_time))
