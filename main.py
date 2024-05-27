import aardvark as adv

# Fluid Object
fluid = adv.fluids.Hydrogen()

# Component 1
fc1 = adv.FlowChannel1D("fc1", adv.Mesh1D(0, 1, 100), 7.2548e-3, 0.4108273402, 0, fluid, hx_type = "use_T_wall")
fc1.inputs.inlet.initial = (300, 1e6, 1e-2)

fc1.inputs.T_wall.initial = 999

# Component 2
# fc2 = adv.FlowChannel1D("fc2", adv.Mesh1D(0, 1, 100), 7.2548e-3, 0.4108273402, 0, he)

# fc2.inputs.inlet = fc2.outputs.outlet

# fc2.inputs.Q_dot.initial = 1e5

adv.solve_steady_state("my_case")

# fc2.outputs.T.plot()
fc1.outputs.T.plot()