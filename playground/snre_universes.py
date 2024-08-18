import openmc
import openmc.model
import numpy as np
import playground.materials as materials


# Is the 1.905 / 1.91 dimensions for flat-to-float with or without the coating?
# According to Schnitzler neutronics paperit is 1.905 WITH coating.

# According to schnitzler TH paper, coolant channels have a diameter of 2.565e-3 BEFORE coating.
# Average coating thickness is 100 microns.
# So, flow diameter is 2.565e-3 - (2*100e-6)
def get_fuel_assembly(id: int, fuel_T: list[float], prop_T: list[float], prop_rho) -> openmc.Universe:

    materials.prop_hydrogen.set_density("g/cm3", prop_rho)

    # Create axial subdivided universes
    axial_prop_universe = _get_axially_subdivided_universe(prop_T, materials.prop_hydrogen)
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

def get_mod_assembly(
        graphite_T: list[float],
        insulator_T: list[float],
        outer_tt_T: list[float],
        mod_T: list[float],
        inner_tt_T: list[float],
        supply_prop_T: list[float],
        return_prop_T: list[float],
        prop_rho: float
    ):

    axial_graphite_universe = _get_axially_subdivided_universe(graphite_T, materials.graphite)
    axial_insulator_universe = _get_axially_subdivided_universe(insulator_T, materials.porous_zrc)
    axial_outer_tt_universe = _get_axially_subdivided_universe(outer_tt_T, materials.inconel718)
    axial_mod_universe = _get_axially_subdivided_universe(mod_T, materials.zrh)
    axial_inner_tt_universe = _get_axially_subdivided_universe(inner_tt_T, materials.inconel718)
    axial_supply_prop_universe = _get_axially_subdivided_universe(supply_prop_T, materials.prop_hydrogen)

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
            cell.fill = mat
            cell.region = regions[i]
            cell.temperature = T[i]

            universe.add_cell(cell)

    return universe
    

if __name__ == "__main__":
    root_universe = get_fuel_assembly(0, 7*[300], [300, 305, 310, 315], 0.001)

    geom = openmc.Geometry(root=root_universe)
    mats = openmc.Materials(materials.all_snre_materials)
    plots = openmc.Plots()

    plot = openmc.Plot()
    plot.basis = "xy"
    plot.width = (2.5, 2.5)
    plot.color_by = "material"
    plot.colors = {
        materials.fuel : (139, 0, 0),
        materials.zrc : (125, 125, 125),
        materials.prop_hydrogen : (0, 0, 139)
    }
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

    

    openmc.plot_geometry()