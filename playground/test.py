import openmc
import openmc.model
import openmc.stats
import numpy as np
import matplotlib.pyplot as plt

L = 100
N = 100
dz = L/N
z_cells = np.array([-L/2 + dz*(i+1) for i in range(N)])
# Try to achieve 0.91321 +/- 0.00037
temperatures = 100*[1950]
#temperatures = 2000*np.cos(z_cells * np.pi/L)+300
plt.plot(z_cells, temperatures)
plt.savefig("test.png")

mats = openmc.Materials()
geom = openmc.Geometry()
settings = openmc.Settings()
tallies = openmc.Tallies()

mat = openmc.Material()
mat.add_element("U", 0.5, "ao", 2.25)
mat.add_element("H", 0.5, "ao")
mat.set_density("g/cm3", 10)
mats.append(mat)

surfs = []

for z in z_cells:
    surfs.append(openmc.ZPlane(z))

regions = openmc.model.subdivide(surfs)

universe = openmc.Universe()
for region, T in zip(regions, temperatures):
    cell = openmc.Cell(region = region, fill = mat)
    cell.temperature = T

    universe.add_cell(cell)

top_z = openmc.ZPlane(z0 = 50)
bottom_z = openmc.ZPlane(z0 = -50)
cyl_or = openmc.ZCylinder(r = 1)

cyl_or.boundary_type = "reflective"
top_z.boundary_type = "vacuum"
bottom_z.boundary_type = "vacuum"

cell = openmc.Cell(fill = universe, region = -top_z & +bottom_z & -cyl_or)
universe = openmc.Universe(cells = [cell])

geom.root_universe = universe

mesh = openmc.RegularMesh()
mesh.dimension = [1, 1, 100]
mesh.lower_left = [-1, -1, -L/2]
mesh.upper_right = [1, 1, L/2]
filter = openmc.MeshFilter(mesh)

tally = openmc.Tally(name = "fission")
tally.scores = ["fission"]
tally.filters = [filter]
tallies.append(tally)

tally = openmc.Tally(name = "delayed-nu-fission")
tally.scores = ["delayed-nu-fission"]
tallies.append(tally)

tally = openmc.Tally(name = "heating")
tally.scores = ["heating"]

tally.filters = [filter]
tallies.append(tally)

plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xz"
plot.width = (2, 110)
plot.pixels = (200, 1000)
plots.append(plot)

uniform_dist = openmc.stats.Box((-1, -1, -L/2), (1, 1, L/2), only_fissionable=True)
settings.source = openmc.IndependentSource(space=uniform_dist)
settings.batches = 100
settings.inactive = 50
settings.particles = 100000
settings.create_delayed_neutrons = False
settings.temperature = {
    "method" : "interpolation"
}

mats.export_to_xml()
geom.export_to_xml()
settings.export_to_xml()
tallies.export_to_xml()
plots.export_to_xml()

#openmc.plot_geometry()
openmc.run()
sp = openmc.StatePoint("statepoint.100.h5")
tally = sp.get_tally(scores = ["fission"])

heating = [tally.mean[i][0][0] for i in range(N)]
heating = [val/sum(heating) for val in heating]

plt.clf()
plt.plot(z_cells, heating)
plt.savefig("test2.png")

with open("results_effective_T.csv", "w") as file:
    for i in range(len(z_cells)-1):
        file.write(str(z_cells[i]) + ", ")

    file.write(str(z_cells[-1]) + "\n")

    for i in range(len(z_cells)-1):
        file.write(str(heating[i]) + ", ")

    file.write(str(heating[-1]))