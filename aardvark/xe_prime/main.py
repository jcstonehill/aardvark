import openmc
import openmc.model
import numpy as np

materials = openmc.Materials()

fuel_universe = openmc.Universe()

fuel_mat = openmc.Material()
fuel_mat.add_element("U", 1.0, "ao")
materials.append(fuel_mat)

coating_mat = openmc.Material()
coating_mat.add_element("Nb", 1.0, "ao")
materials.append(coating_mat)

tierod_mat = openmc.Material()
tierod_mat.add_element("C", 1.0, "ao")
materials.append(tierod_mat)

ss_mat = openmc.Material()
ss_mat.add_element("C", 1.0, "ao")
materials.append(ss_mat)

pyrographite_mat = openmc.Material()
pyrographite_mat.add_element("C", 1.0, "ao")
materials.append(pyrographite_mat)

unfueled_graphite_mat = openmc.Material()
unfueled_graphite_mat.add_element("C", 1.0, "ao")
materials.append(unfueled_graphite_mat)

prop_or = openmc.ZCylinder(r = 0.1213104)
coating_or = openmc.ZCylinder(r = 0.12573)

channel_universe = openmc.Universe()
prop_cell = openmc.Cell(region = -prop_or, fill = None)
coating_cell = openmc.Cell(region = +prop_or & -coating_or, fill = coating_mat)
fuel_cell = openmc.Cell(region = +coating_or, fill = fuel_mat)
channel_universe.add_cells([prop_cell, coating_cell, fuel_cell])

outer_universe = openmc.Universe()
outer_universe.add_cell(openmc.Cell(fill=fuel_mat))

lattice = openmc.HexLattice()
lattice.center = (0., 0.)
lattice.pitch = [0.44]
lattice.outer = outer_universe
lattice.orientation = "x"
lattice.universes = [
    12*[channel_universe],
    6*[channel_universe],
    1*[channel_universe]
]

cell = openmc.Cell(fill = lattice)
fe_universe = openmc.Universe(cells = [cell])
#fuel_outer_surf = openmc.model.HexagonalPrism(edge_length = 1.91516/np.sqrt(3), orientation = "x")
# top = openmc.ZPlane(89/2)
# bottom = openmc.ZPlane(-89/2)
# fuel_outer_surf.boundary_type = "vacuum"
# top.boundary_type = "vacuum"
# bottom.boundary_type = "vacuum"

# fe_universe = openmc.Universe()
# fe_universe.add_cell(openmc.Cell(region = -fuel_outer_surf & +bottom & -top, fill = lattice))

ue_universe = openmc.Universe()

annuli_d = [0.2794, 0.57404, 0.60198, 0.62484, 0.90678, 0.9175496, 0.92456]
annuli_mat = [tierod_mat, None, ss_mat, None, pyrographite_mat, None, coating_mat, unfueled_graphite_mat]

prev_surf = None
for i in range(len(annuli_d)):
    surf = openmc.ZCylinder(r=annuli_d[i]/2)

    if(prev_surf is None):
        region = -surf

    else:
        region = -surf & +prev_surf

    cell = openmc.Cell(region = region, fill = annuli_mat[i])
    ue_universe.add_cell(cell)

    prev_surf = surf

cell = openmc.Cell(region = +prev_surf, fill = annuli_mat[-1])
ue_universe.add_cell(cell)

# ue_outer_surf = openmc.model.HexagonalPrism(edge_length = 1.91516/np.sqrt(3), orientation = "x")
# fuel_outer_surf.boundary_type = "vacuum"

# ue_universe = openmc.Universe()
# cell = openmc.Cell(region = -ue_outer_surf & +bottom & -top, fill = annuli_ue_universe)
# ue_universe.add_cell(cell)

unfueled = openmc.Cell(fill = unfueled_graphite_mat)
unfueled_universe = openmc.Universe(cells = [unfueled])

root = openmc.Universe()

elements = {}

def place_cluster(x, y, loading_codes):
    surf = openmc.model.HexagonalPrism(origin = (x, y), edge_length = 1.91516/np.sqrt(3), orientation = "x")

    cell = openmc.Cell(fill = ue_universe, region = -surf)
    cell.translation = (x, y, 0)
    root.add_cell(cell)

    for i in range(6):
        angle = 2*i*np.pi/6 + np.pi/2
        dx = 1.91516*np.cos(angle)
        dy = 1.91516*np.sin(angle)

        loading_

        # surf = openmc.model.HexagonalPrism(origin = (x+dx, y+dy), edge_length = 1.91516/np.sqrt(3), orientation = "x")
        # cell = openmc.Cell(fill = fe_universe, region = -surf)
        # cell.translation = (x+dx, y+dy, 0)
        # root.add_cell(cell)

f2f = 1.91516
edge = 1.91516/np.sqrt(3)

# 000
place_cluster(0,0)

for i in range(7):
    N = 2+i

    anchor_x = -1.5*(i+1)*edge
    anchor_y = -2.5*(i+1)*f2f

    for j in range(N):
        x = anchor_x+(4.5*j*edge)
        y = anchor_y+(0.5*j*f2f)

        place_cluster(x,y)
        


# A
# place_cluster(-1.5*edge, -2.5*f2f)
# place_cluster(3*edge, -2*f2f)

# # B
# place_cluster(-3*edge, -5*f2f)
# core_lat = openmc.HexLattice()

# r0 = [0]
# r1 = [0]
# r2 = [0, 0]
# r3 = [0, 1, 0]
# r4 = [0, 0, 0, 0]
# r5 = [0, 0, 0, 0, 1]
# r6 = [0, 0, 1, 0, 0, 0]
# r7 = [1, 0, 0, 0, 0, 0, 0]
# r8 = [0, 0, 0, 0, 0, 1, 0, 0]
# r9 = [0, 0, 0, 1, 0, 0, 0, 0, 0]
# r10 = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]

# universe_ids = [r10, r9, r8, r7, r6, r5, r4, r3, r2, r1]

# universes = []

# for ring in universe_ids:
#     new_ring = []

#     for _ in range(6):
#         for i in ring:
#             if(i==1):
#                 new_ring.append(ue_universe)
#             else:
#                 new_ring.append(fe_universe)

#     universes.append(new_ring)

# universes.append([ue_universe])



# universes = [
#     6*[fe_universe],
#     1*[ue_universe]
# ]

# N = 12
# offset = 1
# for i in range(3):
#     universes.insert(0, N*[fe_universe])
#     N += 6

#     ue_ring = []

#     counter = N

#     for _ in range(offset):
#         ue_ring.append(fe_universe)

#     while counter > 0:
#         counter -= 3
#         ue_ring.extend([ue_universe, fe_universe, fe_universe])

#     while(len(ue_ring) > N):
#         ue_ring.pop(-1)

#     universes.insert(0, ue_ring)
#     N += 6

#     universes.insert(0, N*[fe_universe])
#     N += 6 

#     offset += 2

#     if(offset >= 3):
#         offset -= 3
    

# core_lat.center = (0., 0.)
# core_lat.universes = universes
# core_lat.pitch = (1.91516,)
# core_lat.outer = unfueled_universe

# cell = openmc.Cell(fill=core_lat)
# root = openmc.Universe(cells=[cell])

plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xy"
plot.width = (100, 100)
plot.color_by = "material"
plot.pixels = (2000, 2000)
plots.append(plot)

plot = openmc.Plot()
plot.basis = "yz"
plot.width = (2.5, 100)
plot.pixels = (round(2.5*100), 100*100)
plots.append(plot)

model = openmc.Model()
model.materials = materials
model.geometry = openmc.Geometry(root)
model.plots = plots

model.export_to_xml()

openmc.plot_geometry()
