import aardvark as adv
import aardvark.internal_api as adv_int
import matplotlib.pyplot as plt

he = adv.ConstantFluid(0.166, 5192.6,  3115.6, 3.22639e-5, 0.2256)

fc = adv.FlowChannel1D()

fc.inputs.T0_in = 300.
fc.inputs.P0_in = 10e5
fc.inputs.m_dot = 1e-2
fc.inputs.T_wall = 10*[500]

fc.setup.N = 10
fc.setup.A = 7.2548e-3
fc.setup.P_wall = 0.4108273402
fc.setup.L = 1.
fc.setup.eps = 0
fc.setup.fluid = he

fc.check()
adv.solve_steady_state("my_case")

#
# adv.solve_steady_state("my_case")

# fc.solve_steady_state()


# # print(fc.outputs.P.get())
# plt.plot(fc.outputs.node_x.get(), fc.outputs.rho.get())
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)

# plt.show()