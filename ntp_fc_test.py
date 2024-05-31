import aardvark as adv

# Fluid Object
fluid = adv.fluids.IdealGas("my_hydrogen", 14290, 0.18, 2.016, 0.88e-5)
#adv.fluids.IdealGas()
#fluid = adv.fluids.Hydrogen()

# Component 1
fc1 = adv.FlowChannel1D("fc1", adv.Mesh1D(0, 0.89, 100), adv.np.pi*0.0015**2, adv.np.pi*0.0023, 0e-6, fluid, "use_Q_dot")
fc1.inputs.inlet.initial = (372.1, 6e6, 0.0147/19)

fc1.inputs.Q_dot.initial = (0.4e6)/19
fc1.inputs.Q_dot_shape.initial = adv.np.sin(adv.np.linspace(0, 0.89, 99)*adv.np.pi/0.89)

system = adv.System()
system.add_component(fc1)

solver = adv.TransientSolver(system=system)

solver.solve()

# fc2.outputs.T.plot()
fc1.outputs.T.plot()
fc1.outputs.P.plot()