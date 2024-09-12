import openmc
import openmc.model
import numpy as np
import materials
import coupling_data


# Is the 1.905 / 1.91 dimensions for flat-to-float with or without the coating?
# According to Schnitzler neutronics paperit is 1.905 WITH coating.

# According to schnitzler TH paper, coolant channels have a diameter of 2.565e-3 BEFORE coating.
# Average coating thickness is 100 microns.
# So, flow diameter is 2.565e-3 - (2*100e-6)
def get_fuel_assembly(id: int, fuel_T: list[float], prop_T: list[float], prop_mats: list[openmc.Material]) -> openmc.Universe:

    # Create axial subdivided universes
    axial_prop_universe = _get_axially_subdivided_universe(prop_T, prop_mats)
    axial_fuel_universe = _get_axially_subdivided_universe(fuel_T, materials.fuel)
    axial_clad_universe = _get_axially_subdivided_universe(fuel_T, materials.zrc)
    
    # Create channel unit universe
    channel_universe = openmc.Universe()
    
    prop_or = openmc.ZCylinder(r = 0.1228)
    prop_clad_or = openmc.ZCylinder(r = 0.1328)

    prop_cell = openmc.Cell(region = -prop_or, fill = axial_prop_universe)
    prop_clad_cell = openmc.Cell(region = +prop_or & -prop_clad_or, fill = axial_clad_universe)
    fuel_cell = openmc.Cell(region = +prop_clad_or, fill = axial_fuel_universe)

    channel_universe.add_cells([prop_cell, prop_clad_cell, fuel_cell])
    outer_universe = axial_fuel_universe

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

    fa_universe = openmc.Universe(name = "fa" + str(id))
    inner_cell = openmc.Cell(region = -fuel_outer_surf, fill = lattice)
    outer_cell = openmc.Cell(region = +fuel_outer_surf, fill = axial_clad_universe)

    fa_universe.add_cells([inner_cell, outer_cell])

    return fa_universe

def _get_axially_subdivided_universe(T, mat):
    universe = openmc.Universe()

    if(len(T) == 1):
        cell = openmc.Cell(fill = mat)
        cell.temperature = T[0]
        universe.add_cell(cell)

    else:
        dz = 89 / len(T)
        z = -89/2

        surfaces = []

        for i in range(len(T)-1):
            surfaces.append(openmc.ZPlane(z + dz*(i+1)))

        regions = openmc.model.subdivide(surfaces)

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
    
fuel_elements = []

_fe_universe = get_fuel_assembly(
    0,
    coupling_data.fuel_T[0],
    coupling_data.fuel_prop_T[0],
    materials.fuel_prop[0]
)

fuel_elements.append(_fe_universe)

geom = openmc.Geometry(root=fuel_elements[0])
mats = openmc.Materials(materials.all_materials)
plots = openmc.Plots()

plot = openmc.Plot()
plot.basis = "xy"
plot.width = (2.5, 2.5)
plot.color_by = "material"
plot.colors = materials.plotting_colors
plot.pixels = (2000, 2000)

plots.append(plot)

plot = openmc.Plot()
plot.basis = "yz"
plot.width = (2.5, 100)
#plot.color_by = "material"
plots.append(plot)


geom.export_to_xml()
mats.export_to_xml()
plots.export_to_xml()