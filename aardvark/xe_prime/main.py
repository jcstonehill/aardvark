import openmc
import openmc.model
import numpy as np
import matplotlib.pyplot as plt

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

be_mat = openmc.Material()
be_mat.add_element("Be", 1.0, "ao")
materials.append(be_mat)

b4c_mat = openmc.Material()
b4c_mat.add_element("B", 1.0, "ao")
materials.append(b4c_mat)

interface_mat = openmc.Material()
interface_mat.add_element("C", 1.0, "ao")
materials.append(interface_mat)

pv_mat = openmc.Material()
pv_mat.add_element("C", 1.0, "ao")
materials.append(pv_mat)

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

core = openmc.Universe()

fueled_elements = {}
center_elements = {}

def add_cluster_set(center_x, center_y, ring_id, cluster_id):
    # Unfueled Element
    for i in range(6):
        r = np.sqrt(center_x**2 + center_y**2)
        angle0 = np.arctan(center_y/center_x)
        angle = angle0 + i*2*np.pi/6

        x = r*np.cos(angle)
        y = r*np.sin(angle)

        key = str(i+1) + str(ring_id) + "-" + cluster_id + "A"
        center_elements[key] = (x, y)

    element_ids =["B", "C", "D", "E", "F", "G"]

    for j in range(6):
        angle = 2*j*np.pi/6 + np.pi/2
        dx = 1.91516*np.cos(angle)
        dy = 1.91516*np.sin(angle)

        x0 = center_x + dx
        y0 = center_y + dy

        angle0 = np.arctan(y0/x0)

        r = np.sqrt(x0**2 + y0**2)

        for i in range(6):
            angle = angle0 + i*2*np.pi/6
            x = r*np.cos(angle)
            y = r*np.sin(angle)

            key = key = str(i+1) + str(ring_id) + "-" + cluster_id + element_ids[j]
            fueled_elements[key] = (x, y)

# Center Cluster
element_ids =["B", "C", "D", "E", "F", "G"]
center_elements["00-00"] = (0, 0)
for j in range(6):
    angle = 2*j*np.pi/6 + np.pi/2
    dx = 1.91516*np.cos(angle)
    dy = 1.91516*np.sin(angle)

    x0 = dx
    y0 = dy

    angle0 = np.arctan(y0/x0)

    key = key = "00" + "-" + "0" + element_ids[j]
    fueled_elements[key] = (dx, dy)

f2f = 1.91516
edge = 1.91516/np.sqrt(3)

ring_ids = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
for i in range(7):
    N = 1+i

    anchor_x = -3*(i+1)*edge
    anchor_y = -2*(i+1)*f2f

    for j in range(N):
        x = anchor_x+(4.5*j*edge)
        y = anchor_y-(0.5*j*f2f)

        add_cluster_set(x, y, ring_ids[i], str(j+1))

anchor_x = -3*8*edge
anchor_y = -2*8*f2f
x = anchor_x + 4.5*edge
y = anchor_y - 0.5*f2f

add_cluster_set(x, y, "J", str(3))

for i in range(5):
    x = anchor_x + (4.5*(2+i)*edge)
    y = anchor_y - (0.5*(2+i)*f2f)

    add_cluster_set(x, y, "H", str(i+3))

x = anchor_x + (4.5*(2+5)*edge)
y = anchor_y - (0.5*(2+5)*f2f)

add_cluster_set(x, y, "J", str(9))

def add_fuel_element(x0, y0, suffix):
    angle0 = np.arctan(y0/x0)

    r = np.sqrt(x0**2 + y0**2)

    for i in range(6):
        angle = angle0 + i*2*np.pi/6
        x = r*np.cos(angle)
        y = r*np.sin(angle)

        key = key = str(i+1) + suffix
        fueled_elements[key] = (x, y)

def add_center_element(x0, y0, suffix):
    angle0 = np.arctan(y0/x0)

    r = np.sqrt(x0**2 + y0**2)

    for i in range(6):
        angle = angle0 + i*2*np.pi/6
        x = r*np.cos(angle)
        y = r*np.sin(angle)

        key = key = str(i+1) + suffix
        center_elements[key] = (x, y)

# Add irregular clusters
anchor_x = -3*8*edge
anchor_y = -2*8*f2f

# C1
x = anchor_x + 1.5*edge
y = anchor_y - 1.5*f2f
add_fuel_element(x, y, "J-3J")
x = anchor_x + 1.5*edge
y = anchor_y - 2.5*f2f
add_fuel_element(x, y, "J-3H")

# C2
x = anchor_x + 3*edge
y = anchor_y - 2*f2f
add_center_element(x, y, "J-3AA")
x = anchor_x + 3*edge
y = anchor_y - 3*f2f
add_fuel_element(x, y, "J-3N")

# C3
x = anchor_x + 4.5*edge
y = anchor_y - 2.5*f2f
add_fuel_element(x, y, "J-3S")
x = anchor_x + 4.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-3T")

# C4
x = anchor_x + 6*edge
y = anchor_y - 2*f2f
add_fuel_element(x, y, "J-3R")
x = anchor_x + 6*edge
y = anchor_y - 3*f2f
add_center_element(x, y, "J-3AAA")
x = anchor_x + 6*edge
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-3U")

# C5
x = anchor_x + 7.5*edge
y = anchor_y - 2.5*f2f
add_fuel_element(x, y, "J-3W")
x = anchor_x + 7.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-3V")
x = anchor_x + 7.5*edge
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-4M")

# C6
x = anchor_x + 9*edge
y = anchor_y - 3*f2f
add_fuel_element(x, y, "J-4C")
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-4D")
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-4H")

# # C7
x = anchor_x + 10.5*edge
y = anchor_y - 2.5*f2f
add_fuel_element(x, y, "J-4B")
y = anchor_y - 3.5*f2f
add_center_element(x, y, "J-4A")
y = anchor_y - 4.5*f2f
add_center_element(x, y, "J-4AA")

# C8
x = anchor_x + 12*edge
y = anchor_y - 3*f2f
add_fuel_element(x, y, "J-4G")
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-4F")
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-4K")

# C9
x = anchor_x + 13.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-5C")
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-5D")
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-5H")

# C10
x = anchor_x + 15*edge
y = anchor_y - 3*f2f
add_fuel_element(x, y, "J-5B")
y = anchor_y - 4*f2f
add_center_element(x, y, "J-5A")
y = anchor_y - 5*f2f
add_center_element(x, y, "J-5AA")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-5J")

# C11
x = anchor_x + 16.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-5G")
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-5F")
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-5K")

# C12
x = anchor_x + 18*edge
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-6C")
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-6D")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-6H")

# C13
x = anchor_x + 19.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-6B")
y = anchor_y - 4.5*f2f
add_center_element(x, y, "J-6A")
y = anchor_y - 5.5*f2f
add_center_element(x, y, "J-6AA")

# C14
x = anchor_x + 21*edge
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-6G")
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-6F")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-6K")

# C15
x = anchor_x + 22.5*edge
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-7C")
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-7D")
y = anchor_y - 6.5*f2f
add_fuel_element(x, y, "J-7H")

# C16
x = anchor_x + 24*edge
y = anchor_y - 4*f2f
add_fuel_element(x, y, "J-7B")
y = anchor_y - 5*f2f
add_center_element(x, y, "J-7A")
y = anchor_y - 6*f2f
add_center_element(x, y, "J-7AA")

# C17
x = anchor_x + 25.5*edge
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-7G")
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-7F")
y = anchor_y - 6.5*f2f
add_fuel_element(x, y, "J-7K")

# C18
x = anchor_x + 27*edge
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-8C")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-8D")

# C19
x = anchor_x + 28.5*edge
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-8B")
y = anchor_y - 5.5*f2f
add_center_element(x, y, "J-8A")

# C20
x = anchor_x + 30*edge
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-8G")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-8F")

# C21
x = anchor_x + 31.5*edge
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-9K")

# C22
x = anchor_x + 33*edge
y = anchor_y - 5*f2f
add_center_element(x, y, "J-8AA")
y = anchor_y - 6*f2f
add_fuel_element(x, y, "J-9H")

# C23
x = anchor_x + 34.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-9R")
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-9S")
y = anchor_y - 5.5*f2f
add_fuel_element(x, y, "J-9P")

# C24
x = anchor_x + 36*edge
y = anchor_y - 3*f2f
add_fuel_element(x, y, "J-9W")
y = anchor_y - 4*f2f
add_center_element(x, y, "J-8AAA")
y = anchor_y - 5*f2f
add_fuel_element(x, y, "J-9T")

# C25
x = anchor_x + 37.5*edge
y = anchor_y - 3.5*f2f
add_fuel_element(x, y, "J-9V")
y = anchor_y - 4.5*f2f
add_fuel_element(x, y, "J-9U")




region = None

for pos in center_elements.values():
    surf = openmc.model.HexagonalPrism(origin = pos, edge_length = 1.91516/np.sqrt(3), orientation = "x")
    cell = openmc.Cell(region = -surf, fill = ue_universe)
    cell.translation = (pos[0], pos[1], 0)
    core.add_cell(cell)

    if(region is None):
        region = -surf

    else:
        region = region & -surf

for pos in fueled_elements.values():
    surf = openmc.model.HexagonalPrism(origin = pos, edge_length = 1.91516/np.sqrt(3), orientation = "x")
    cell = openmc.Cell(region = -surf, fill = fe_universe)
    cell.translation = (pos[0], pos[1], 0)
    core.add_cell(cell)

    region = region & -surf




outer_cell = openmc.Cell(region = ~region, fill = unfueled_graphite_mat)
core.add_cell(outer_cell)

cd_fill_universe = openmc.Universe()
cd_or = openmc.ZCylinder(r = 4.76+0.125)
poison_ir = openmc.ZCylinder(r = 4.5)
#poison_ir = openmc.ZCylinder(r = 4.76)
poison_plane1 = openmc.YPlane()
poison_plane2 = openmc.Plane.from_points([0, 0, 0], [-0.5, 0.866025, 0], [-0.5, 0.866025, 1])

poison_region = +poison_plane1 & +poison_plane2 & +poison_ir & -cd_or
cd_region = ~poison_region & -cd_or
cd_flow_region = +cd_or

cd_fill_universe.add_cell(openmc.Cell(region = cd_region, fill = be_mat))
cd_fill_universe.add_cell(openmc.Cell(region = poison_region, fill = b4c_mat))
cd_fill_universe.add_cell(openmc.Cell(region = cd_flow_region, fill = None))

core_or = openmc.ZCylinder(r=2.54*17.785)
interface_or = openmc.ZCylinder(r = 2.54*40/2)
gap1_or = openmc.ZCylinder(r=50.96637)
refl_or = openmc.ZCylinder(r=62.69863)
gap2_or = openmc.ZCylinder(r=2.54*49.562/2)
pv_or = openmc.ZCylinder(r=2.54*50.530/2)
pv_or.boundary_type = "vacuum"
root = openmc.Universe()
core_cell = openmc.Cell(fill = core, region = -core_or)
root.add_cell(core_cell)

interface_cell = openmc.Cell(fill = interface_mat, region = +core_or & -interface_or)
gap1_cell = openmc.Cell(fill = None, region = -gap1_or & +interface_or)
root.add_cells([interface_cell, gap1_cell])

refl_region = +gap1_or & -refl_or

cd_angle = 90

for i in range(12):
    angle0 = 0

    angle = angle0 + 2*np.pi*i/12
    x = 56.8325*np.cos(angle)
    y = 56.8325*np.sin(angle)

    surf = openmc.ZCylinder(x, y, r = 5.42798)

    refl_region = refl_region & +surf

    cell = openmc.Cell(region = -surf, fill = cd_fill_universe)
    cell.translation = (x, y, 0)
    cell.rotation = (0, 0, i*360/12 + 120 - cd_angle)

    root.add_cell(cell)

cell = openmc.Cell(region = refl_region, fill = be_mat)
root.add_cell(cell)

cell = openmc.Cell(region = +refl_or & -gap2_or, fill = None)
root.add_cell(cell)

cell = openmc.Cell(region = +gap2_or & -pv_or, fill = pv_mat)
root.add_cell(cell)



fig = plt.figure()
ax = fig.add_subplot()
plt.grid(True)
ax.set_aspect("equal")

x = []
y = []

for pos in fueled_elements.values():
    x.append(pos[0])
    y.append(pos[1])

plt.plot(x,y, ".")

x = []
y = []

for pos in center_elements.values():
    x.append(pos[0])
    y.append(pos[1])

plt.plot(x,y, ".")


plt.savefig("elements.png")

colors = {
    
}

plots = openmc.Plots()
plot = openmc.Plot()
plot.basis = "xy"
plot.width = (15, 15)
plot.color_by = "material"
plot.pixels = (2000, 2000)
plots.append(plot)

# plot = openmc.Plot()
# plot.basis = "yz"
# plot.width = (2.5, 100)
# plot.pixels = (round(2.5*100), 100*100)
# plots.append(plot)

settings = openmc.Settings()
settings.batches = 100
settings.inactive = 50
settings.particles = 10000

model = openmc.Model()
model.materials = materials
model.geometry = openmc.Geometry(root)
model.plots = plots
model.settings = settings

model.export_to_xml()

openmc.plot_geometry()

#openmc.run()