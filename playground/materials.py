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


# Mod Supply Prop
mod_supply_prop: list[list] = []

for set in coupling_data.mod_supply_prop_rho:
    mod_supply_prop.append([])

    for rho in set:
        _mat = openmc.Material(name = "Mod Supply Prop")
        _mat.set_density("g/cm3", rho)
        _mat.add_element("H", 1.0, "ao")

        mod_supply_prop[-1].append(_mat)
        all_materials.append(_mat)

        plotting_colors[_mat] = _color_dark_blue

# Mod Return Prop
mod_return_prop: list[list] = []

for set in coupling_data.mod_return_prop_rho:
    mod_return_prop.append([])

    for rho in set:
        _mat = openmc.Material(name = "Mod Return Prop")
        _mat.set_density("g/cm3", rho)
        _mat.add_element("H", 1.0, "ao")

        mod_return_prop[-1].append(_mat)
        all_materials.append(_mat)

        plotting_colors[_mat] = _color_dark_blue

# (U,Zr)C-Graphite
fuel = openmc.Material(name = "(U,Zr)C-Graphite")
fuel.set_density("g/cm3", 3.64)

fuel.add_nuclide("U234",     0.001736,    "wo")
fuel.add_nuclide("U235",     0.153584,    "wo")
fuel.add_nuclide("U236",     0.000340,    "wo")
fuel.add_nuclide("U238",     0.009176,    "wo")

fuel.add_nuclide("C12",      0.333888,    "wo")
fuel.add_nuclide("C13",      0.004024,    "wo")

fuel.add_nuclide("Zr90",     0.252215,    "wo")
fuel.add_nuclide("Zr91",     0.055614,    "wo")
fuel.add_nuclide("Zr92",     0.085942,    "wo")
fuel.add_nuclide("Zr94",     0.088991,    "wo")
fuel.add_nuclide("Zr96",     0.014490,    "wo")

all_materials.append(fuel)
plotting_colors[fuel] = _color_dark_red


# ZrC
zrc = openmc.Material(name = "ZrC")
zrc.set_density("g/cm3", 6.73)

zrc.add_element("Zr", 0.5, "ao")
zrc.add_element("C", 0.5, "ao")

all_materials.append(zrc)
plotting_colors[zrc] = _color_lighter_grey


# Insulator
porous_zrc = openmc.Material(name = "Porous ZrC")
porous_zrc.set_density("g/cm3", 3.365)

porous_zrc.add_element("Zr", 0.5, "ao")
porous_zrc.add_element("C", 0.5, "ao")

all_materials.append(porous_zrc)
plotting_colors[porous_zrc] = _color_dark_grey


# ZrH
zrh = openmc.Material(name = "ZrH")
zrh.set_density("g/cm3", 5.587)

zrh.add_element("Zr", 0.33333, "ao")
zrh.add_element("H", 0.66667, "ao")

all_materials.append(zrh)
plotting_colors[zrh] = _color_darker_grey


# Be
be = openmc.Material(name = "Be")
be.set_density("g/cm3", 1.848)

be.add_element("Be", 1.0, "ao")

all_materials.append(be)


# Stainless Steel 347
ss = openmc.Material(name = "Stainless Steel 347")
ss.set_density("g/cm3", 7.960)

ss.add_element("Cr", 0.18, "wo")
ss.add_element("Ni", 0.11, "wo")
ss.add_element("Fe", 0.71, "wo")

all_materials.append(ss)


# Aluminum
al = openmc.Material(name = "Aluminum")
al.set_density("g/cm3", 2.7)

al.add_element("Al", 1.0, "ao")

all_materials.append(al)


# Smeared Beryllium Barrel
be_barrel = openmc.Material(name = "Smeared Beryllium Barrel")
be_barrel.set_density("g/cm3", 1.5214)

be_barrel.add_element("Be", 0.91764, "wo")
be_barrel.add_element("Fe", 0.08236, "wo")

all_materials.append(be_barrel)


# Smeared Lower Tie Tube Plenum
low_tt_plen = openmc.Material(name = "Smeared Lower Tie Tube Plenum")
low_tt_plen.set_density("g/cm3", 0.3908)

low_tt_plen.add_element("H", 0.00742, "wo")
low_tt_plen.add_element("Fe", 0.99258, "wo")

all_materials.append(low_tt_plen)


# Smeared Core Support Plate
core_support_plate = openmc.Material(name = "Smeared Core Support Plate")
core_support_plate.set_density("g/cm3", 1.005)

core_support_plate.add_element("H", 0.00209, "wo")
core_support_plate.add_element("Fe", 0.99791, "wo")

all_materials.append(core_support_plate)


# Smeared Upper Tie Tube Plenum
up_tt_plen = openmc.Material(name = "Smeared Upper Tie Tube Plenum")
up_tt_plen.set_density("g/cm3", 0.9718)

up_tt_plen.add_element("H", 0.00216, "wo")
up_tt_plen.add_element("Fe", 0.99784, "wo")

all_materials.append(up_tt_plen)


# Borated Zirconium Hydride
borated_zrh = openmc.Material(name = "Borated Zirconium Hydride")
borated_zrh.set_density("g/cm3", 4.45190)

borated_zrh.add_element("H", 0.02053, "wo")
borated_zrh.add_element("B", 0.00494, "wo")
borated_zrh.add_element("Zr", 0.97453, "wo")

all_materials.append(borated_zrh)


# Plenum Hydrogen
plenum_hydrogen = openmc.Material(name = "Plenum Hydrogen")
plenum_hydrogen.set_density("g/cm3", 0.0027)

plenum_hydrogen.add_element("H", 1.0, "ao")

all_materials.append(plenum_hydrogen)
plotting_colors[plenum_hydrogen] = _color_dark_blue


# Smeared CD Actuator
cd_actuator = openmc.Material(name = "Smeared CD Actuator")
cd_actuator.set_density("g/cm3", 0.4279)

cd_actuator.add_element("H", 0.0022, "wo")
cd_actuator.add_element("Fe", 0.278, "wo")
cd_actuator.add_element("Cu", 0.1477, "wo")

all_materials.append(cd_actuator)


# Inconel 718
inconel718 = openmc.Material(name = "Inconel 718")
inconel718.set_density("g/cm3", 8.22)

inconel718.add_element("Cr", 0.190, "wo")
inconel718.add_element("Ni", 0.530, "wo")
inconel718.add_element("Mo", 0.031, "wo")
inconel718.add_element("Nb", 0.026, "wo")
inconel718.add_element("Ta", 0.026, "wo")
inconel718.add_element("Fe", 0.197, "wo")

all_materials.append(inconel718)
plotting_colors[inconel718] = _color_dark_grey


# Graphite
graphite = openmc.Material(name = "Graphite")
graphite.set_density("g/cm3", 2.26)

graphite.add_element("C", 1.0, "ao")

all_materials.append(graphite)
plotting_colors[graphite] = _color_darker_grey


# Poison
poison = openmc.Material(name = "Hafnium")
poison.set_density("g/cm3", 13.07)

poison.add_element("Hf", 1.0, "ao")

all_materials.append(poison)
plotting_colors[poison] = _color_black