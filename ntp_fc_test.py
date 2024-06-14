import aardvark as adv


fluid = adv.fluids.IdealGas("my_hydrogen", 14290, 0.18, 2.016, 0.88e-5)

fc1 = adv.FlowChannel1D("fc1", adv.Mesh1D(0, 0.89, 100), adv.np.pi*0.0015**2, adv.np.pi*0.0023, 0e-6, fluid, "use_Q_dot")

fc1.inlet.initial = (372.1, 6e6, 0.0147/19)
fc1.outlet.initial = (372.1, 6e6, 0.0147/19)

fc1.Q_dot.initial = (0.18e6)/19
fc1.Q_dot_shape.initial = adv.np.sin(adv.np.linspace(0, 0.89, 99)*adv.np.pi/0.89)
fc1.T_wall.initial = 500

fc1.T.initial = 500
fc1.P.initial = 101325

fc2 = adv.FlowChannel1D("fc2", adv.Mesh1D(0, 0.89, 100), adv.np.pi*0.0015**2, adv.np.pi*0.0023, 0e-6, fluid, "use_Q_dot")
fc2.inlet.initial = (372.1, 6e6, 0.0147/19)
fc2.outlet.initial = (372.1, 6e6, 0.0147/19)

fc2.Q_dot.initial = (0.18e6)/19
fc2.Q_dot_shape.initial = adv.np.sin(adv.np.linspace(0, 0.89, 99)*adv.np.pi/0.89)
fc2.T_wall.initial = 500

fc2.T.initial = 500
fc2.P.initial = 101325

system = adv.System()
system.add_component(fc2)
system.add_component(fc1)

system.connect(fc1.outlet, fc2.inlet)

solver = adv.TransientSolver("my_case", system)

solver.solve()

fc1.T.plot()
fc2.T.plot()

fc1.P.plot()
fc2.P.plot()