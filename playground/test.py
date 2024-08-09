import openmc

mats = openmc.Materials()
geom = openmc.Geometry()
settings = openmc.Settings()
tallies = openmc.Tallies()

mat = openmc.Material()
mat.add_element("U", 0.5, "ao", 2.25)
mat.add_element("H", 0.5, "ao")
mat.set_density("g/cm3", 10)
mats.append(mat)

top_z = openmc.ZPlane(z0 = 50)
bottom_z = openmc.ZPlane(z0 = -50)
cyl_or = openmc.ZCylinder(r = 1)

cyl_or.boundary_type = "reflective"
top_z.boundary_type = "vacuum"
bottom_z.boundary_type = "vacuum"

cell = openmc.Cell(fill = mat, region = -top_z & +bottom_z & -cyl_or)
universe = openmc.Universe(cells = [cell])

geom.root_universe = universe

tally = openmc.Tally(name = "fission")
tally.scores = ["fission"]
mesh = openmc.RegularMesh()
mesh.dimension = (1, 1, 10)
mesh.lower_left = (-1, -1, -50)
mesh.upper_right = (1, 1, 50)
filter = openmc.MeshFilter(mesh)
tally.filters = [filter]
tallies.append(tally)

settings.batches = 100
settings.inactive = 50
settings.particles = 100000

mats.export_to_xml()
geom.export_to_xml()
settings.export_to_xml()
tallies.export_to_xml()

openmc.run()

