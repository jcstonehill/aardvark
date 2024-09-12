import openmc

import coupling_data

_color_black = (0, 0, 0)
_color_white = (255, 255, 255)
_color_dark_grey = (135, 135, 135)
_color_darker_grey = (95, 95 ,95)
_color_light_grey = (175, 175, 175)
_color_lighter_grey = (215, 215, 215)
_color_dark_blue = (0, 0, 135)
_color_dark_red = (135, 0, 0)
_color_dark_green = (0, 95, 0)

plotting_colors = {}

all_materials = openmc.Materials()

# Fuel Prop
fuel_prop: list[list] = []

for set in coupling_data.fuel_prop_rho:
    fuel_prop.append([])

    for rho in set:
        _mat = openmc.Material(name = "Fuel Prop")
        _mat.set_density("g/cm3", rho)
        _mat.add_element("H", 1.0, "ao")

        fuel_prop[-1].append(_mat)
        all_materials.append(_mat)

        plotting_colors[_mat] = _color_dark_blue

# (U,Zr)C-Graphite
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

all_materials.append(fuel)
plotting_colors[fuel] = _color_dark_red


# ZrC
zrc = openmc.Material(name = "ZrC")
zrc.set_density("g/cm3", 6.73)

zrc.add_element("Zr", 0.5, "ao")
zrc.add_element("C", 0.5, "ao")

all_materials.append(zrc)
plotting_colors[zrc] = _color_lighter_grey