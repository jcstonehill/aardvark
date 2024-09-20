import openmc
import openmc.model
import numpy as np

import universes
import materials

def generate_xml():
    lattice = openmc.HexLattice()

    rings: list[list] = []

    # There are a total of 19 rings.
    # Ring 0 (Outermost Ring)
    rings.append((18*6)*[universes.filler_element])

    # Ring 1
    rings.append([])
    for _ in range(6):
        rings[-1].extend(7*[universes.filler_element])
        rings[-1].extend(4*[universes.fuel_elements[1]])
        rings[-1].extend(6*[universes.filler_element])

    # Ring 2
    rings.append([])
    for _ in range(6):
        rings[-1].extend(3*[universes.filler_element])
        rings[-1].extend(5*[universes.fuel_elements[2]])
        rings[-1].extend(1*[universes.moderator_elements[2]])
        rings[-1].extend(5*[universes.fuel_elements[2]])
        rings[-1].extend(2*[universes.filler_element])

    # Ring 3
    rings.append([])
    for _ in range(6):
        rings[-1].extend([universes.filler_element])
        rings[-1].extend(2*[universes.fuel_elements[3]])
        rings[-1].extend([universes.moderator_elements[3]])
        rings[-1].extend(2*[universes.fuel_elements[3]])
        rings[-1].extend([universes.moderator_elements[3]])
        rings[-1].extend(2*[universes.fuel_elements[3]])
        rings[-1].extend([universes.moderator_elements[3]])
        rings[-1].extend(2*[universes.fuel_elements[3]])
        rings[-1].extend([universes.moderator_elements[3]])
        rings[-1].extend(2*[universes.fuel_elements[3]])
    
    # Ring 4
    rings.append([])
    for _ in range(6):
        rings[-1].extend([universes.fuel_elements[4]])
        rings[-1].extend([universes.moderator_elements[4]])
        for __ in range(4):
            rings[-1].extend(2*[universes.fuel_elements[4]])
            rings[-1].extend([universes.moderator_elements[4]])

    # Ring 5
    rings.append([])
    for _ in range(6):
        for __ in range(4):
            rings[-1].extend(2*[universes.fuel_elements[5]])
            rings[-1].extend(1*[universes.moderator_elements[5]])
        rings[-1].extend(1*[universes.fuel_elements[5]])    
    
    # Ring 6
    rings.append([])
    for _ in range(6):
        for __ in range(4):
            rings[-1].extend(1*[universes.moderator_elements[6]])
            rings[-1].extend(2*[universes.fuel_elements[6]])

    # Ring 7
    rings.append([])
    for _ in range(6):
        rings[-1].extend(1*[universes.fuel_elements[7]])
        rings[-1].extend(1*[universes.moderator_elements[7]])

        for __ in range(3):
            rings[-1].extend(2*[universes.fuel_elements[7]])
            rings[-1].extend(1*[universes.moderator_elements[7]])

    # Ring 8
    rings.append([])
    for _ in range(6):
        for __ in range(3):
            rings[-1].extend(2*[universes.fuel_elements[8]])
            rings[-1].extend(1*[universes.moderator_elements[8]])
        rings[-1].extend(1*[universes.fuel_elements[8]])

    # Ring 9
    rings.append([])
    for _ in range(6):
        for __ in range(3):
            rings[-1].extend(1*[universes.moderator_elements[9]])
            rings[-1].extend(2*[universes.fuel_elements[9]])

    # Ring 10 FIRST RING WITH ANY ORANGE
    rings.append([])
    for _ in range(6):
        rings[-1].extend(1*[universes.fuel_elements[10]])
        rings[-1].extend(1*[universes.moderator_elements[10]])
        for __ in range(2):
            rings[-1].extend(2*[universes.fuel_elements[10]])
            rings[-1].extend(1*[universes.moderator_elements[10]])
    
    # Ring 11
    rings.append([])
    for _ in range(6):
        for __ in range(2):
            rings[-1].extend(2*[universes.fuel_elements[11]])
            rings[-1].extend(1*[universes.moderator_elements[11]])
        rings[-1].extend(1*[universes.fuel_elements[11]])
        
    # Ring 12
    rings.append([])
    for _ in range(6):
        for __ in range(2):
            rings[-1].extend(1*[universes.moderator_elements[12]])
            rings[-1].extend(2*[universes.fuel_elements[12]])
    
    # Ring 13
    rings.append([])
    for _ in range(6):
        rings[-1].extend(1*[universes.fuel_elements[13]])
        rings[-1].extend(1*[universes.moderator_elements[13]])
        rings[-1].extend(2*[universes.fuel_elements[13]])
        rings[-1].extend(1*[universes.moderator_elements[13]])

    # Ring 14
    rings.append([])
    for _ in range(6):
        rings[-1].extend(2*[universes.fuel_elements[14]])
        rings[-1].extend(1*[universes.moderator_elements[14]])
        rings[-1].extend(1*[universes.fuel_elements[14]])

    # Ring 15
    rings.append([])
    for _ in range(6):
        rings[-1].extend(1*[universes.moderator_elements[15]])
        rings[-1].extend(2*[universes.fuel_elements[15]])
    
    # Ring 16
    rings.append([])
    for _ in range(6):
        rings[-1].extend(1*[universes.fuel_elements[16]])
        rings[-1].extend(1*[universes.moderator_elements[16]])

    # Ring 17
    rings.append(6*[universes.fuel_elements[17]])

    # Ring 18
    rings.append([universes.moderator_elements[17]])

    lattice.center = (0., 0.)
    lattice.pitch = (1.905,)
    lattice.universes = rings
    lattice.outer = universes.filler_element
    lattice.orientation = "y"

    core = openmc.Universe()

    core_or = openmc.ZCylinder(r=29.5275)
    cell = openmc.Cell(region = -core_or, fill = lattice)
    core.add_cell(cell)

    outer_gap1_or = openmc.ZCylinder(r=29.8450)
    cell = openmc.Cell(region = -outer_gap1_or & + core_or, fill = materials.plenum_hydrogen)
    core.add_cell(cell)

    outer_wrapper_or = openmc.ZCylinder(r=30.1625)
    cell = openmc.Cell(region = -outer_wrapper_or & + outer_gap1_or, fill = materials.ss)
    core.add_cell(cell)

    outer_gap2_or = openmc.ZCylinder(r=30.48)
    cell = openmc.Cell(region = -outer_gap2_or & + outer_wrapper_or, fill = materials.plenum_hydrogen)
    core.add_cell(cell)

    outer_be_barrel_or = openmc.ZCylinder(r=33.3375)
    cell = openmc.Cell(region = -outer_be_barrel_or & +outer_gap2_or, fill = materials.be_barrel)
    core.add_cell(cell)

    outer_gap3_or = openmc.ZCylinder(r=33.6550)
    cell = openmc.Cell(region = -outer_gap3_or & +outer_be_barrel_or, fill = materials.plenum_hydrogen)
    core.add_cell(cell)

    # Control Drums
    outer_refl_or = openmc.ZCylinder(r=48.3870)
    refl_region = +outer_gap3_or & -outer_refl_or

    cd_universe = openmc.Universe()
    #vane = openmc.model.CylinderSector(5.3975, 6.0325, 0, 120)
    vane = openmc.model.CylinderSector(4, 6.0325, 0, 120)
    poison_cell = openmc.Cell(region = -vane, fill = None)
    cd_cell = openmc.Cell(region = +vane & -vane.outer_cyl, fill = materials.be)
    h_cell = openmc.Cell(region = +vane.outer_cyl, fill = materials.plenum_hydrogen)

    cd_universe.add_cells([poison_cell, cd_cell, h_cell])

    refl_mid_r = (48.387+33.655)/2

    cd_angle = 0
    for i in range(12):
        theta = (i/12)*2*np.pi
        
        x = refl_mid_r * np.cos(theta)
        y = refl_mid_r * np.sin(theta)

        cd_or = openmc.ZCylinder(x0 = x, y0 = y, r = 6.1325)
        cell = openmc.Cell(region = -cd_or, fill = cd_universe)
        cell.translation = (x, y, 0)
        cell.rotation = (0, 0, theta*180/np.pi + 120 - cd_angle)
        core.add_cell(cell)
        refl_region = refl_region & +cd_or





 

    
    cell = openmc.Cell(region = -outer_refl_or & +outer_gap3_or, fill = materials.be)
    core.add_cell(cell)

    outer_gap4_or = openmc.ZCylinder(r=48.7045)
    cell = openmc.Cell(region = -outer_gap4_or & +outer_refl_or, fill=materials.plenum_hydrogen)
    core.add_cell(cell)

    
    cell = openmc.Cell(region = +outer_gap4_or, fill = materials.al)
    
    core.add_cell(cell)

    root_universe = openmc.Universe()
    top = openmc.ZPlane(89.9/2)
    top.boundary_type = "vacuum"

    bottom = openmc.ZPlane(-89.9/2)
    bottom.boundary_type = "vacuum"

    outer_pv_or = openmc.ZCylinder(r=49.2633)
    outer_pv_or.boundary_type = "vacuum"

    cell = openmc.Cell(region = +bottom & -top & -outer_pv_or, fill = core)
    root_universe.add_cell(cell)

    geometry = openmc.Geometry(root_universe)
    geometry.export_to_xml()
    materials.all_materials.export_to_xml()

    plots = openmc.Plots()

    plot = openmc.Plot()
    plot.basis = "xy"
    plot.width = (110, 110)
    plot.color_by = "material"
    #plot.colors = materials.plotting_colors
    plot.pixels = (2000, 2000)

    plots.append(plot)

    plots.export_to_xml()

    openmc.plot_geometry()

if __name__ == "__main__":
    generate_xml()

    settings = openmc.Settings()
    settings.batches = 100
    settings.inactive = 50

    settings.particles = 10000
    settings.temperature = {
        "method" : "interpolation"
    }
    settings.export_to_xml()

    openmc.run()