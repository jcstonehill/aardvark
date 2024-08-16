import openmc

# Define materials
mats = openmc.Materials()

# (U, Zr)C-Graphite
mat = openmc.Material()
mat.set_density("g/cm3", 3.64)

mat.add_nuclide("U234",     0.00022,    "ao")
mat.add_nuclide("U235",     0.01906,    "ao")
mat.add_nuclide("U236",     0.00004,    "ao")
mat.add_nuclide("U238",     0.00112,    "ao")
mat.add_nuclide("C12",      0.81148,    "ao")
mat.add_nuclide("C13",      0.00909,    "ao")
mat.add_nuclide("Zr90",     0.08180,    "ao")
mat.add_nuclide("Zr91",     0.01784,    "ao")
mat.add_nuclide("Zr92",     0.02727,    "ao")
mat.add_nuclide("Zr94",     0.02763,    "ao")
mat.add_nuclide("Zr96",     0.00445,    "ao")


# ZrC
mat = openmc.Material()
mat.set_density("g/cm3", 6.73)
mat.add_element("Zr", 0.5, "ao")
mat.add_element("C", 0.5, "ao")

vals = mat.get_nuclide_atom_densities()

total = 0
for key in vals.keys():
    total += float(vals[key])

for key in vals.keys():
    print(key, vals[key]/total)




# total = mat.get_mass_density()
# nuclides = ["U234", "U235", "U236", "U238", "C12", "C13", "Zr90", "Zr91", "Zr92", "Zr94", "Zr96"]

for key in nuclides:
    print(key, mat.get_mass(key)/total)

mats.append(mat)
mats.export_to_xml()