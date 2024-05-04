import openmc
import openmc.model
import numpy as np

cc_r = openmc.ZCylinder(r=0.128)

mat1 = openmc.Material()
mat1.add_elements_from_formula("H2O")

mat2 = openmc.Material()
mat2.add_elements_from_formula("UC")

materials = openmc.Materials([mat1, mat2])
materials.export_to_xml()

outer_universe = openmc.Universe()


theta = -90
orig_plane1 = openmc.Plane.from_points((0, 0, 0), (np.cos(np.pi*theta/180), np.sin(np.pi*theta/180), 0), (0, 0, -1))
plane1 = orig_plane1
for i in range(11):
    theta += 30

    plane2 = openmc.Plane.from_points((0, 0, 0), (np.cos(np.pi*theta/180), np.sin(np.pi*theta/180), 0), (0, 0, -1))

    cell = openmc.Cell(fill = mat1, region = +plane1 & -plane2)
    outer_universe.add_cell(cell)

    plane1 = plane2

outer_universe.add_cell(openmc.Cell(fill=mat1, region = +plane1 & -orig_plane1))


cc_cell = openmc.Cell(region = -cc_r, fill = mat1)
fuel_cell = openmc.Cell(region = +cc_r, fill = mat2)

universe = openmc.Universe(cells = [cc_cell, fuel_cell])

lat = openmc.HexLattice()

lat.pitch = [0.40894]
lat.universes = [12*[universe], 6*[universe], [universe]]
lat.center = (0, 0)
lat.outer = outer_universe
lat.orientation = "x"

outer_surface = openmc.model.HexagonalPrism(edge_length=1.1, orientation = "x")
outer_surface.boundary_type = "vacuum"

cell = openmc.Cell(region = -outer_surface, fill = outer_universe)

root_universe = openmc.Universe(cells=[cell])
#root_universe.plot()
geometry = openmc.Geometry()
geometry.root_universe = root_universe

geometry.export_to_xml()





plot1 = openmc.Plot()
plot1.filename = "plot1.png"
plot1.color_by = "cell"
plot1.pixels = (1000, 1000)
plot1.width = (2.2, 2.2)
plot1.basis = "xy"

plots = openmc.Plots([plot1])
plots.export_to_xml()

openmc.plot_geometry()