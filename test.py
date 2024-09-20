import gmsh

gmsh.initialize()
gmsh.model.add("test")
gmsh.model.occ.add_sphere(0, 0, 0, 5)
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate()
data = []
vn = gmsh.view.add("test")

elementTypes, elementTags, nodeTags = gmsh.model.mesh.get_elements(dim=3)
nodes, coord, _ = gmsh.model.mesh.getNodes()
node_coords = {}
for i in range(len(nodes)):
    x = float(coord[i])
    y = float(coord[i+1])
    z = float(coord[i+2])
    node_coords[int(nodes[i])] = (x, y, z)

data = []
for i in range(len(elementTags[0])):
    elementTag = elementTags[0][i]

    x = 0
    y = 0
    z = 0

    for j in range(4):
        nodeTag = nodeTags[0][4*i+j]

        coords = node_coords[nodeTag]

        x += 0.25*coords[0]
        y += 0.25*coords[1]
        z += 0.25*coords[2]

    data.append((elementTag, y))

gmsh.view.add_model_data(vn, 0, "test", "ElementData", elementTags[0], data)

#gmsh.fltk.run()
gmsh.write("myfile.msh")


gmsh.finalize()

# for val in nodeTags:
#     print(len(val))