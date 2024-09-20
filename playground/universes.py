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

def get_mod_assembly(
        id: int,
        mod_T: list[float],
        supply_prop_T: list[float],
        return_prop_T: list[list],
        supply_prop_mats: list[openmc.Material],
        return_prop_mats: list[openmc.Material]
        ):
    
    axial_clad_universe = _get_axially_subdivided_universe(mod_T, materials.zrc)
    axial_graphite_universe = _get_axially_subdivided_universe(mod_T, materials.graphite)
    axial_insulator_universe = _get_axially_subdivided_universe(mod_T, materials.porous_zrc)
    axial_tt_universe = _get_axially_subdivided_universe(mod_T, materials.inconel718)
    axial_mod_universe = _get_axially_subdivided_universe(mod_T, materials.zrh)
    axial_gap_universe = _get_axially_subdivided_universe(mod_T, materials.plenum_hydrogen)
    
    axial_supply_prop_universe = _get_axially_subdivided_universe(supply_prop_T, supply_prop_mats)
    axial_return_prop_universe = _get_axially_subdivided_universe(return_prop_T, return_prop_mats)

    ma_universe = openmc.Universe(name = "ma" + str(id))

    elem_outer_surf = openmc.model.HexagonalPrism(edge_length = 1.895/np.sqrt(3), orientation = "x")
    gap3_or = openmc.ZCylinder(r = 0.81280)
    ins_or = openmc.ZCylinder(r = 0.80645)
    gap2_or = openmc.ZCylinder(r = 0.70485)
    out_tt_or = openmc.ZCylinder(r = 0.69850)
    return_or = openmc.ZCylinder(r = 0.67818)
    mod_or = openmc.ZCylinder(r = 0.58420)
    gap1_or = openmc.ZCylinder(r = 0.26670)
    in_tt_or = openmc.ZCylinder(r = 0.26035)
    supply_or = openmc.ZCylinder(r = 0.20955)

    ma_universe.add_cell(openmc.Cell(region = +elem_outer_surf, fill = axial_clad_universe))
    ma_universe.add_cell(openmc.Cell(region = -elem_outer_surf & +gap3_or, fill = axial_graphite_universe))
    ma_universe.add_cell(openmc.Cell(region = -gap3_or & +ins_or, fill = axial_gap_universe))
    ma_universe.add_cell(openmc.Cell(region = -ins_or & +gap2_or, fill = axial_insulator_universe))
    ma_universe.add_cell(openmc.Cell(region = -gap2_or & +out_tt_or, fill = axial_gap_universe))
    ma_universe.add_cell(openmc.Cell(region = -out_tt_or & +return_or, fill = axial_tt_universe))
    ma_universe.add_cell(openmc.Cell(region = -return_or & +mod_or, fill = axial_return_prop_universe))
    ma_universe.add_cell(openmc.Cell(region = -mod_or & +gap1_or, fill = axial_mod_universe))
    ma_universe.add_cell(openmc.Cell(region = -gap1_or & +in_tt_or, fill = axial_gap_universe))
    ma_universe.add_cell(openmc.Cell(region = -in_tt_or & +supply_or, fill = axial_tt_universe))
    ma_universe.add_cell(openmc.Cell(region = -supply_or, fill = axial_supply_prop_universe))

    return ma_universe

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
    
fuel_elements = [None]
moderator_elements = [None]

for i in range(17):
    _fe_universe = get_fuel_assembly(
        i,
        coupling_data.fuel_T[i],
        coupling_data.fuel_prop_T[i],
        materials.fuel_prop[i]
    )

    _me_universe = get_mod_assembly(
        i,
        coupling_data.mod_T[i],
        coupling_data.mod_supply_prop_T[i],
        coupling_data.mod_return_prop_T[i],
        materials.mod_supply_prop[i],
        materials.mod_return_prop[i]
    )

    fuel_elements.append(_fe_universe)
    moderator_elements.append(_me_universe)

filler_element = openmc.Universe(cells = [openmc.Cell(fill = materials.be)])

if __name__ == "__main__":
    geom = openmc.Geometry(root=moderator_elements[0])
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

    

    openmc.plot_geometry()