import openmc

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


# ZrC
zrc = openmc.Material(name = "ZrC")
zrc.set_density("g/cm3", 6.73)

zrc.add_element("Zr", 0.5, "ao")
zrc.add_element("C", 0.5, "ao")


# ZrH
zrh = openmc.Material(name = "ZrH")
zrh.set_density("g/cm3", 5.587, "ao")

zrh.add_element("Zr", 0.33333, "ao")
zrh.add_element("H", 0.66667, "ao")


# Be
be = openmc.Material(name = "Be")
be.set_density("g/cm3", 1.848)

be.add_element("Be", 1.0, "ao")


# Stainless Steel 347
ss = openmc.Material(name = "Stainless Steel 347")
ss.set_density("g/cm3", 7.960)

ss.add_element("Cr", 0.18, "wo")
ss.add_element("Ni", 0.11, "wo")
ss.add_element("Fe", 0.71, "wo")


# Gaseous Hydrogen
h = openmc.Material()
h.set_density("g/cm3", 0.00008)

h.add_element("H", 1.0, "ao")


# Aluminum
al = openmc.Material(name = "Aluminum")
al.set_density("g/cm3", 2.7)

al.add_element("Al", 1.0, "ao")


# Smeared Beryllium Barrel
be_barrel = openmc.Material(name = "Smeared Beryllium Barrel")
be_barrel.set_density("g/cm3", 1.5214)

be_barrel.add_element("Be", 0.91764, "wo")
be_barrel.add_element("Fe", 0.08236, "wo")


# Smeared Lower Tie Tube Plenum
low_tt_plen = openmc.Material(name = "Smeared Lower Tie Tube Plenum")
low_tt_plen.set_density("g/cm3", 0.3908)

low_tt_plen.add_element("H", 0.00742, "wo")
low_tt_plen.add_element("Fe", 0.99258, "wo")


# Smeared Core Support Plate
core_support_plate = openmc.Material(name = "Smeared Core Support Plate")
core_support_plate.set_density("g/cm3", 1.005)

core_support_plate.add_element("H", 0.00209, "wo")
core_support_plate.add_element("Fe", 0.99791, "wo")


# Smeared Upper Tie Tube Plenum
up_tt_plen = openmc.Material(name = "Smeared Upper Tie Tube Plenum")
up_tt_plen.set_density("g/cm3", 0.9718)

up_tt_plen.add_element("H", 0.00216, "wo")
up_tt_plen.add_element("Fe", 0.99784, "wo")


# Borated Zirconium Hydride
borated_zrh = openmc.Material(name = "Borated Zirconium Hydride")
borated_zrh.set_density("g/cm3", 4.45190)

borated_zrh.add_element("H", 0.02053, "wo")
borated_zrh.add_element("B", 0.00494, "wo")
borated_zrh.add_element("Zr", 0.97453, "wo")


# Plenum Hydrogen
plenum_hydrogen = openmc.Material(name = "Plenum Hydrogen")
plenum_hydrogen.set_density("g/cm3", 0.0027)

plenum_hydrogen.add_element("H", 1.0, "ao")


# Smeared CD Actuator
cd_actuator = openmc.Material(name = "Smeared CD Actuator")
cd_actuator.set_density("g/cm3", 0.4279)

cd_actuator.add_element("H", 0.0022, "wo")
cd_actuator.add_element("Fe", 0.278, "wo")
cd_actuator.add_element("Cu", 0.1477, "wo")


all_snre_materials = [
    fuel, zrc, zrh, be, ss, h, al, be_barrel,
    low_tt_plen, core_support_plate, up_tt_plen, 
    borated_zrh, plenum_hydrogen, cd_actuator]