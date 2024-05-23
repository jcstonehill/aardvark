import aardvark as adv
import aardvark.internal_api as adv_int
import matplotlib.pyplot as plt
import numpy as np

he = adv.ConstantFluid(0.166, 5192.6,  3115.6, 3.22639e-5, 0.2256)
#he = adv.ConstantFluid()

fc = adv.FlowChannel1D("my_fc", np.linspace(0, 1, 10), 7.2548e-3, 0.4108273402, 0, he)

# heat_from_wall = adv.HeatTransferFromWall("heated_wall", np.linspace(0, 1, 100), 0.4108273402)
# fc2.inputs.Q_dot = heat_from_wall.outputs.Q_dot
# heat_from_wall.inputs.T_flow = fc2.outputs.T
# heat_from_wall.inputs.htc = fc2.outputs.htc
# heat_from_wall.inputs.T_wall.initial = 3000

fc.inputs.T0_in.initial = 300
fc.inputs.P0_in.initial = 10e5
fc.inputs.m_dot.initial = 1e-2
#fc.inputs.Q_dot.initial = 100*[1000]

wall = adv.HeatTransferFromWall("wall", np.linspace(0, 1, 10), 0.4108273402)
wall.inputs.T_flow = fc.outputs.T
wall.inputs.htc = fc.outputs.htc
wall.inputs.T_wall.initial = 3000

fc.inputs.Q_dot = wall.outputs.Q_dot



adv.solve_steady_state("my_case")

fc.outputs.T.plot()