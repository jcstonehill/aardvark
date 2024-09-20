import gmsh
import math

gmsh.initialize()

def GenerateFuelElement(x, y, flatToFlat):
    diagonal = flatToFlat/math.cos(math.pi/6)

    hexagonPoints = []

    hexagonPoints.append(gmsh.model.occ.addPoint(x+0.5*diagonal,y,0))
    hexagonPoints.append(gmsh.model.occ.addPoint(x+0.25*diagonal,y+0.5*flatToFlat,0))
    hexagonPoints.append(gmsh.model.occ.addPoint(x-0.25*diagonal,y+0.5*flatToFlat,0))
    hexagonPoints.append(gmsh.model.occ.addPoint(x-0.5*diagonal,y,0))
    hexagonPoints.append(gmsh.model.occ.addPoint(x-0.25*diagonal,y-0.5*flatToFlat,0))
    hexagonPoints.append(gmsh.model.occ.addPoint(x+0.25*diagonal,y-0.5*flatToFlat,0))

    hexagonLines = []
    for j in range(len(hexagonPoints)):
        hexagonLines.append(gmsh.model.occ.addLine(hexagonPoints[j-1], hexagonPoints[j]))
        gmsh.model.occ.synchronize()
        gmsh.model.mesh.set_transfinite_curve(hexagonLines[-1], 15)

    pitch = 0.0041
    cc1 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x, y, 0, 0.00115)])
    cc2 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+pitch, y, 0, 0.00115)])
    cc3 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+2*pitch, y, 0, 0.00115)])
    cc4 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-pitch, y, 0, 0.00115)])
    cc5 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-2*pitch, y, 0, 0.00115)])

    cc6 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+0.5*pitch, y+pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc7 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+1.5*pitch, y+pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc8 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-0.5*pitch, y+pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc9 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-1.5*pitch, y+pitch*math.cos(math.pi/6), 0, 0.00115)])

    cc10 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+0.5*pitch, y-pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc11 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+1.5*pitch, y-pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc12 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-0.5*pitch, y-pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc13 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-1.5*pitch, y-pitch*math.cos(math.pi/6), 0, 0.00115)])
    
    cc14 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x, y+2*pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc15 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+pitch, y+2*pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc16 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-pitch, y+2*pitch*math.cos(math.pi/6), 0, 0.00115)])

    cc17 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x, y-2*pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc18 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x+pitch, y-2*pitch*math.cos(math.pi/6), 0, 0.00115)])
    cc19 = gmsh.model.occ.addCurveLoop([gmsh.model.occ.addCircle(x-pitch, y-2*pitch*math.cos(math.pi/6), 0, 0.00115)])

    hexagonOuter = gmsh.model.occ.addCurveLoop(hexagonLines)

    gmsh.model.occ.synchronize()
    
    gmsh.model.occ.addPlaneSurface([hexagonOuter, cc1, cc2, cc3, cc4, cc5, cc6, cc7, cc8, cc9, cc10, cc11, cc12, cc13, cc14, cc15, cc16, cc17, cc18, cc19])
    gmsh.model.occ.addPlaneSurface([cc1])
    gmsh.model.occ.addPlaneSurface([cc2])
    gmsh.model.occ.addPlaneSurface([cc3])
    gmsh.model.occ.addPlaneSurface([cc4])
    gmsh.model.occ.addPlaneSurface([cc5])
    gmsh.model.occ.addPlaneSurface([cc6])
    gmsh.model.occ.addPlaneSurface([cc7])
    gmsh.model.occ.addPlaneSurface([cc8])
    gmsh.model.occ.addPlaneSurface([cc9])
    gmsh.model.occ.addPlaneSurface([cc10])
    gmsh.model.occ.addPlaneSurface([cc11])
    gmsh.model.occ.addPlaneSurface([cc12])
    gmsh.model.occ.addPlaneSurface([cc13])
    gmsh.model.occ.addPlaneSurface([cc14])
    gmsh.model.occ.addPlaneSurface([cc15])
    gmsh.model.occ.addPlaneSurface([cc16])
    gmsh.model.occ.addPlaneSurface([cc17])
    gmsh.model.occ.addPlaneSurface([cc18])
    gmsh.model.occ.addPlaneSurface([cc19])

    gmsh.model.occ.extrude(gmsh.model.occ.get_entities(2), 0, 0, 0.89, numElements = [25])

GenerateFuelElement(0, 0, 1.905/100)

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate()
gmsh.write("snre.msh")
gmsh.fltk.run()