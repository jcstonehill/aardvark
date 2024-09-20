import meshio
import numpy as np

mesh: meshio.Mesh = meshio.read("myfile.msh")
mesh.cells = [mesh.cells[4]]
data = {
    "test" : [1*np.linspace(0, 1, 640)]
}
mesh = meshio.Mesh(cells = mesh.cells, points = mesh.points, cell_data=data)

#mesh.cell_data["y"] = 
meshio.write("myfile.vtk", mesh)