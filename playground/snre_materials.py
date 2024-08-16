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


