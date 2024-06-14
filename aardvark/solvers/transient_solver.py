from aardvark.base.system import System
from aardvark.base.log import Log

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

class TransientSolver:
    def __init__(self, case_name = "Case", system: System = None, 
                 duration: float = 1, dt: float = 1, tol = 1e-6, max_iter = 100):
        self.case_name = case_name
        self.system = system
        self.duration = duration
        self.dt = dt
        self.tol = tol
        self.max_iter = max_iter

    def solve(self):
        System.create_outputs_dir(self.case_name)

        Log.message("Setting up system...")
        self.system.setup()

        Log.message("Starting solution loop.")

        start_time = time.time()

        Log.line_break()
        self.system.march()
        self.system.solve(self.dt, self.tol, self.max_iter)
        Log.line_break()

        end_time = time.time()

        Log.message("Computation Time was " + convert_computation_time(end_time-start_time))
