import aardvark as adv
import matplotlib.pyplot as plt

he = adv.ConstantFluid(0.166, 5192.6,  3115.6, 3.22639e-5, 0.2256)
Nu_cor = adv.DittusBoelterNuCorrelation()
ff_cor = adv.ColebrookWhiteFFCorrelation()

fc = adv.FlowChannel1D(
    N = 10, 
    A = 7.2548e-3,
    P_wall = 0.4108273402,
    L = 5,
    eps = 0,
    fluid = he,
    Nu_cor = Nu_cor,
    ff_cor = ff_cor
)

fc.inputs.T0_in = 300
fc.inputs.P0_in = 10e5
fc.inputs.m_dot = 1e-2
fc.opt_inputs.T_wall = 10*[500]

fc.check()

fc.solve_steady_state()

print(fc.outputs.P.get())
plt.plot(fc.outputs.node_x.get(), fc.outputs.P.get())

#ax.ticklabel_format(useOffset=False)

plt.show()
# plt.savefig("plot.png")