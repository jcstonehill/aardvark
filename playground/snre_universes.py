import openmc
import openmc.model
import snre_materials


# Is the 1.905 / 1.91 dimensions for flat-to-float with or without the coating?
# According to Schnitzler neutronics paperit is 1.905 WITH coating.

# According to schnitzler TH paper, coolant channels have a diameter of 2.565e-3 BEFORE coating.
# Average coating thickness is 100 microns.
# So, flow diameter is 2.565e-3 - (2*100e-6)
def get_fuel_assembly(id: int, fuel_T: list[float], prop_T: list[float], prop_rho: list[float]) -> openmc.Universe:

    # Create propellant universe
    prop_universe = openmc.Universe(name = "propellant" + str(id))
    dz = 0.89 / len(prop_T)

    z = -0.89/2

    surfaces = []

    for i in range(len(prop_T)):
        top = openmc.ZPlane(z0 = z + dz)
        bottom = openmc.ZPlane(z0 = z + dz)


        


    outer_clad = openmc.model.hexagonal_prism(edge_length = 1.09985)
    outer_fuel = openmc.model.hexagonal_prism(edge_length = 1.09408)

