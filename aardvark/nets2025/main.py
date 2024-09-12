import openmc
import universes

model = openmc.Model()
model.geometry = universes.geom
model.materials = universes.mats
model.plots = universes.plots

mesh = openmc.RegularMesh()
mesh

settings = openmc.Settings()
settings.create_fission_neutrons = False
