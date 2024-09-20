import openmc
import openmc.model
import openmc.source
import numpy as np
import matplotlib.pyplot as plt
import openmc.stats

model = openmc.model.Model()

# Define materials.
fuel = openmc.Material(name='UO2 (2.4%)')
fuel.set_density('g/cm3', 10.29769)
fuel.add_nuclide('U234', 4.4843e-6)
fuel.add_nuclide('U235', 5.5815e-4)
fuel.add_nuclide('U238', 2.2408e-2)
fuel.add_nuclide('O16', 4.5829e-2)

clad = openmc.Material(name='Zircaloy')
clad.set_density('g/cm3', 6.55)
clad.add_nuclide('Zr90', 2.1827e-2)
clad.add_nuclide('Zr91', 4.7600e-3)
clad.add_nuclide('Zr92', 7.2758e-3)
clad.add_nuclide('Zr94', 7.3734e-3)
clad.add_nuclide('Zr96', 1.1879e-3)

hot_water = openmc.Material(name='Hot borated water')
hot_water.set_density('g/cm3', 1.785)
hot_water.add_nuclide('H1', 4.9457e-2)
hot_water.add_nuclide('O16', 2.4672e-2)
hot_water.add_nuclide('B10', 8.0042e-6)
hot_water.add_nuclide('B11', 3.2218e-5)
hot_water.add_s_alpha_beta('c_H_in_H2O')

# Define the materials file.
model.materials.extend((fuel, clad, hot_water))

# Instantiate ZCylinder surfaces
pitch = 1.26
fuel_or = openmc.ZCylinder(x0=0, y0=0, r=0.39218, name='Fuel OR')
clad_or = openmc.ZCylinder(x0=0, y0=0, r=0.45720, name='Clad OR')
left = openmc.XPlane(x0=-pitch/2, name='left', boundary_type='reflective')
right = openmc.XPlane(x0=pitch/2, name='right', boundary_type='reflective')
bottom = openmc.YPlane(y0=-pitch/2, name='bottom',
                        boundary_type='reflective')
top = openmc.YPlane(y0=pitch/2, name='top', boundary_type='reflective')

# Instantiate Cells
fuel_pin = openmc.Cell(name='Fuel', fill=fuel)
cladding = openmc.Cell(name='Cladding', fill=clad)
water = openmc.Cell(name='Water', fill=hot_water)

# Use surface half-spaces to define regions
fuel_pin.region = -fuel_or
cladding.region = +fuel_or & -clad_or
water.region = +clad_or & +left & -right & +bottom & -top

# Create root universe
model.geometry.root_universe = openmc.Universe(0, name='root universe')
model.geometry.root_universe.add_cells([fuel_pin, cladding, water])

model.settings.batches = 10
model.settings.inactive = 5
model.settings.particles = 100
model.settings.source = openmc.IndependentSource(
    space=openmc.stats.Box([-pitch/2, -pitch/2, -1], [pitch/2, pitch/2, 1]),
    constraints={'fissionable': True}
)

model.settings.particles = 100
model.settings.batches = 100
model.settings.inactive = 50

# source = openmc.source.IndependentSource()
# source.space = openmc.stats.Point()

# model.settings.source = source
# model.settings.run_mode = "fixed source"
# model.settings.create_fission_neutrons = True
# model.settings.create_delayed_neutrons = False

# times = np.linspace(0, 0.1, 100)
tallies = openmc.Tallies()
# filter = openmc.TimeFilter(times)
# tally = openmc.Tally()
# tally.scores = ["total"]
# tally.filters = [filter]
# tallies.append(tally)

# tally = openmc.Tally(name = "nu-fission")
# tally.scores = ["nu-fission"]
# tallies.append(tally)

tally = openmc.Tally()
mesh = openmc.RegularMesh()
mesh.lower_left = (-pitch/2, -pitch/2, -pitch/2)
mesh.upper_right = (pitch/2, pitch/2, pitch/2)
mesh.dimension = (1, 1, 10)
tally.scores = ["flux"]
filter = openmc.MeshFilter(mesh)
tally.filters = [filter]
tallies.append(tally)

model.geometry.export_to_xml()
model.materials.export_to_xml()
model.settings.export_to_xml()
tallies.export_to_xml()

openmc.run()

sp = openmc.StatePoint("statepoint.100.h5")

tally: openmc.Tally = sp.get_tally(scores = ["total"])

vals = []
for val in tally.mean:
    vals.append(val[0][0])

times = [0.5*times[i] + 0.5*times[i+1] for i in range(len(times)-1)]

plt.plot(times, vals)
plt.savefig("test.png")

tally: openmc.Tally = sp.get_tally(scores = ["nu-fission"])
print(tally.mean)