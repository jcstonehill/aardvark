import aardvark as adv
import aardvark.internal_api as adv_int
import matplotlib.pyplot as plt
import numpy as np

he = adv.ConstantFluid(0.166, 5192.6,  3115.6, 3.22639e-5, 0.2256)

fc2 = adv.FlowChannel1D("my_fc2", np.linspace(0, 1, 100), 7.2548e-3, 0.4108273402, 0, he)
fc3 = adv.FlowChannel1D("my_fc3", np.linspace(0, 1, 100), 7.2548e-3, 0.4108273402, 0, he)
fc = adv.FlowChannel1D("my_fc", np.linspace(0, 1, 100), 7.2548e-3, 0.4108273402, 0, he)

fc.inputs.T0_in.initial = 300
fc.inputs.P0_in.initial = 10e5
fc.inputs.m_dot.initial = 1e-2
fc.inputs.Q_dot.initial = 100*[1000]

fc2.inputs.T0_in = fc.outputs.T0_out
fc2.inputs.P0_in = fc.outputs.P0_out
fc2.inputs.m_dot = fc.outputs.m_dot

fc3.inputs.T0_in = fc2.outputs.T0_out
fc3.inputs.P0_in = fc2.outputs.P0_out
fc3.inputs.m_dot = fc2.outputs.m_dot

adv.solve_steady_state("my_case")