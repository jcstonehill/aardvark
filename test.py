import aardvark.internal_api as adv
import numpy as np

print(adv.functions.laminar_friction_factor(1000))
print(adv.functions.churchill(150-6, 3e-4, 1000))
my_func = adv.functions.churchill

print(my_func(150e-6, 3e-4, 1000))