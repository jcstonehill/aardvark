import openmc
import openmc.model
import openmc.mesh
import openmc.source
import openmc.stats
import numpy as np
import matplotlib.pyplot as plt

fidelity = 1
I = 20
J = 20
K = 20

N = I*J*K

T_fuel = [300, 300]
T_prop = [300, 300]
rho_prop = [0.07, 0.07]

poison_frac = 0.0029

# Start Creating Case
model = openmc.Model()

fuel = openmc.Material(name = "(U,Zr)C-Graphite")
fuel.set_density("g/cm3", 3.64)
fuel.add_nuclide("U234",     0.00022,    "ao")
fuel.add_nuclide("U235",     0.01906,    "ao")
fuel.add_nuclide("U236",     0.00004,    "ao")
fuel.add_nuclide("U238",     0.00112,    "ao")
fuel.add_nuclide("C12",      0.81148,    "ao")
fuel.add_nuclide("C13",      0.00909,    "ao")
fuel.add_nuclide("Zr90",     0.08180,    "ao")
fuel.add_nuclide("Zr91",     0.01784,    "ao")
fuel.add_nuclide("Zr92",     0.02727,    "ao")
fuel.add_nuclide("Zr94",     0.02763,    "ao")
fuel.add_nuclide("Zr96",     0.00445,    "ao")
fuel.add_nuclide("B10",     poison_frac, "ao")

zrc = openmc.Material(name = "ZrC")
zrc.set_density("g/cm3", 6.73)
zrc.add_element("Zr", 0.5, "ao")
zrc.add_element("C", 0.5, "ao")

h = []
for rho in rho_prop:
    mat = openmc.Material()
    mat.add_element("H", 1.0, "ao")
    mat.set_density("g/cm3", rho)
    h.append(mat)

materials = openmc.Materials()
materials.append(fuel)
materials.append(zrc)
materials.extend(h)
model.materials = materials

def get_axially_subdivided_universe(T, mat):
    universe = openmc.Universe()

    if(len(T) == 1):
        cell = openmc.Cell(fill = mat)
        cell.temperature = T[0]
        universe.add_cell(cell)

    else:
        dz = 89 / len(T)
        z0 = -89/2

        surfaces = []

        for i in range(len(T)+1):
            surfaces.append(openmc.ZPlane(z0+i*dz))

        surfaces[0].boundary_type = "vacuum"
        surfaces[-1].boundary_type = "vacuum"

        regions = openmc.model.subdivide(surfaces)
        regions.pop(0)
        regions.pop(-1)

        for i in range(len(regions)):
            cell = openmc.Cell()
            cell.region = regions[i]
            cell.temperature = T[i]

            if(type(mat) is list):
                cell.fill = mat[i]

            else:
                cell.fill = mat

            universe.add_cell(cell)

    return universe

prop_universe = get_axially_subdivided_universe(T_prop, h)
clad_universe = get_axially_subdivided_universe(T_fuel, zrc)
fuel_universe = get_axially_subdivided_universe(T_fuel, fuel)

channel_universe = openmc.Universe()

prop_or = openmc.ZCylinder(r = 0.1228)
prop_clad_or = openmc.ZCylinder(r = 0.1328)

prop_cell = openmc.Cell(region = -prop_or, fill = prop_universe)
prop_clad_cell = openmc.Cell(region = +prop_or & -prop_clad_or, fill = clad_universe)
fuel_cell = openmc.Cell(region = +prop_clad_or, fill = fuel_universe)

channel_universe.add_cells([prop_cell, prop_clad_cell, fuel_cell])
outer_universe = fuel_universe

# Create fuel assembly lattice.
lattice = openmc.HexLattice()
lattice.center = (0., 0.)
lattice.pitch = [0.40894]
lattice.outer = outer_universe
lattice.orientation = "x"
lattice.universes = [
    12*[channel_universe],
    6*[channel_universe],
    1*[channel_universe]
]

fuel_outer_surf = openmc.model.HexagonalPrism(edge_length = 1.895/np.sqrt(3), orientation = "x")
clad_outer_surf = openmc.model.HexagonalPrism(edge_length = 1.905/np.sqrt(3), orientation = "x")
clad_outer_surf.boundary_type = "reflective"


fa_universe = openmc.Universe()
inner_cell = openmc.Cell(region = -fuel_outer_surf, fill = lattice)
outer_cell = openmc.Cell(region = +fuel_outer_surf & -clad_outer_surf, fill = clad_universe)

fa_universe.add_cells([inner_cell, outer_cell])

model.geometry = openmc.Geometry(fa_universe)

mesh = openmc.mesh.RegularMesh()
mesh.dimension = (I, J, K)
mesh.lower_left = (-1.1, -1.1, -89/2)
mesh.upper_right = (1.1, 1.1, 89/2)

meshfilter = openmc.MeshFilter(mesh)

times = np.linspace(0, 0.00012, 20)
timefilter = openmc.TimeFilter(times)

tallies = openmc.Tallies()
tally = openmc.Tally()
tally.scores = ["fission"]
tally.filters = [meshfilter, timefilter]
tallies.append(tally)

model.tallies = tallies

plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xy"
plot.width = (2.5, 2.5)
plot.color_by = "material"
plot.pixels = (2000, 2000)
plots.append(plot)

plot = openmc.Plot()
plot.basis = "yz"
plot.width = (2.5, 100)
plot.pixels = (round(2.5*100), 100*100)
plots.append(plot)

model.plots = plots

mesh_i = 30
source = openmc.IndependentSource()
strengths = N*[0]
strengths[mesh_i] = 1
space = openmc.stats.MeshSpatial(mesh, strengths)
source.space = space

settings = openmc.Settings()
#settings.run_mode = "fixed source"
#settings.source = source
settings.batches = 100
settings.particles = 10000
settings.create_fission_neutrons = True
settings.create_delayed_neutrons = True
model.settings = settings

model.export_to_xml()

openmc.run()

sp = openmc.StatePoint("statepoint.100.h5")
tally: openmc.Tally = sp.get_tally(scores = ["fission"])

df = tally.get_pandas_dataframe()

df.to_csv("results.csv")