"""
Author: Keshawn Boughton
This attempts to first plot a rectangle of the dimensions of a given image with 'holes'
made from the convex hulls made in ConvexHullTakeTwo.py.
Code for triangulation used from: https://shapely.readthedocs.io/en/2.1.2/reference/shapely.constrained_delaunay_triangles.html
Code for visualization used from https://stackoverflow.com/questions/8919719/how-to-plot-a-complex-polygon
"""

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import shapely
import ConvexHullTakeTwo as imgConv

newImage = imgConv.getImage()
img_contours, img_hier = imgConv.prepImage(newImage)
hulls = imgConv.makeConvexHulls(img_contours, img_hier, newImage)
# print(newImage.shape)

"""Given a sequence of Geometric objects (Shapely exlcusive object)
This reformats them into properly readable coordinate points. It returns a list of a list of tuples!"""
def formatPolyPts(polyTri):
    polyPts = []
    for i in range(len(polyTri.geoms)):
        polyPts.append([])
        x, y = polyTri.geoms[i].exterior.xy
        for j in range(len(x)-1):
            polyPts[i].append((x[j], y[j]))
    return polyPts


"""Given a list of tuples representing the exterior points and
a list of list of tuples representing the interior points (these represent the holes),
it formats the points in a way that's properly compatible with plotting."""
def makePathFriendly(extPts, interPts):
    ptList = extPts.copy()
    actList = []
    for i in range(len(extPts)):
        if i==0:
            actList.append(Path.MOVETO)
        else:
            actList.append(Path.LINETO)
    ptList.append((0, 0))
    actList.append(Path.CLOSEPOLY)
    for i in range(len(interPts)):
        for j in range(len(interPts[i])):
            if j==0:
                actList.append(Path.MOVETO)
            else:
                actList.append(Path.LINETO)
            ptList.append(interPts[i][j])
        actList.append(Path.CLOSEPOLY)
        ptList.append((0, 0))
    return ptList, actList

# This part displays the classroom polygon with holes and saves it as "img_hole.png"
# axes = plt.gca()
# ext = [(0, 0), (0, newImage.shape[0]), (newImage.shape[1], newImage.shape[0]), (newImage.shape[1], 0)]
# inter = hulls
# points, actions = makePathFriendly(ext, inter)
# path = Path(points, actions)
# patch = PathPatch(path)
# axes.set_xlim(0,newImage.shape[1])
# axes.set_ylim(0,newImage.shape[0])
# axes.add_patch(patch)

# plt.savefig("img_hole.png")

# makes polygon of classroom with hulls as holes
points = shapely.Polygon([(0, 0), (0, newImage.shape[0]), (newImage.shape[1], newImage.shape[0]), (newImage.shape[1], 0)], holes=hulls)
triPoints = shapely.constrained_delaunay_triangles(points).normalize() # the triangulation!
triPtsList = formatPolyPts(triPoints)

# This part displays the TRIANGULATION of the classroom polygon with holes and saves it as "img_triangulation.png"
# axesTwo = plt.gca()
# for coords in triPtsList: # iterates through triangles in triangulation
#     pathCoords = coords.copy()
#     pathCoords.append((0, 0))
#     path = Path(pathCoords, [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
#     patch = PathPatch(path)
#     axesTwo.add_patch(patch)
# axesTwo.set_xlim(0,newImage.shape[1])
# axesTwo.set_ylim(0,newImage.shape[0])

# plt.savefig("img_tringulate.png")
# plt.close("all")

"""Start of centroil computation from CDT"""
def makeCentroids(triPts):
    centroidsCDT = []
    for tri in triPts.geoms:
        cent = shapely.centroid(tri)
        centroidsCDT.append((cent.x, cent.y))
    return centroidsCDT

print(len(triPoints.geoms))
