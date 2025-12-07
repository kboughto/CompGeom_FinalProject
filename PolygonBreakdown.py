"""
Author: Keshawn Boughton & Nadezhda Dominguez Salinas
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
import networkx as nx

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

"""
Given the sequence of Triangules (again, Shapely exclusive object) and the hull points (in the form of a list of a list of tuples),
This creates the graph such that its edges do not leave the triangulated polygon.
Returns a graph made with Networkx.
"""
def createCentroidGraph(triangles, hullPts):
    centGraph = nx.Graph()
    
    # Adding the centroids of the CDT as nodes in the graph
    for i, tri in enumerate(triangles.geoms):
        c = shapely.centroid(tri)
        centGraph.add_node(i, pos = (c.x, c.y))

    # Adding the edges between centroids of adjacent triangles
    for i in range(len(triangles.geoms)):
        for j in range(i+1, len(triangles.geoms)):
            firstTri = triangles.geoms[i]
            secondTri = triangles.geoms[j]

            # For adjacent triangles add an edge
            if firstTri.intersects(secondTri) and firstTri.boundary.intersects(secondTri.boundary):
                firstTriCentroid = firstTri.centroid
                secondTriCentroid = secondTri.centroid
                centroidLine = shapely.LineString([(firstTriCentroid.x, firstTriCentroid.y), (secondTriCentroid.x, secondTriCentroid.y)])
                if not lineIntersectsPoly(centroidLine, hullPts):
                    distCentroids = firstTriCentroid.distance(secondTriCentroid)
                    centGraph.add_edge(i,j, weight = distCentroids)
    
    return centGraph

"""
Given the sequence of Triangles, it computes its centroids and stores them as a list of tuples.
"""
def makeCentroids(triPts):
    centroidsCDT = []
    for tri in triPts.geoms:
        cent = shapely.centroid(tri)
        centroidsCDT.append((cent.x, cent.y))
    return centroidsCDT

"""
Given a LineString and a list of list of coordinates as tuples,
it checks whether the line intersects any of the hulls.
"""
def lineIntersectsPoly(line, polyCoords):
    for hull in polyCoords:
        hulPoly = shapely.Polygon(hull)
        if hulPoly.boundary.intersects(line):
            return True
    return False

"""Finding the closest centroid to the point in the classroom environment"""
def closestCent(centroids, point):
    x,y = point
    bestCent = 0
    bestDist = float("inf")

    for i in range(len(centroids)):
        d = (((x-centroids[i][0])**2) + ((y-centroids[i][1])**2))**0.5
        if d < bestDist:
            bestDist = d
            bestCent = i
    return bestCent

def getShortestPathCoords(hullPts, img):
    points = shapely.Polygon([(0, 0), (0, newImage.shape[0]), (newImage.shape[1], newImage.shape[0]), (newImage.shape[1], 0)], holes=hulls)
    triPoints = shapely.constrained_delaunay_triangles(points).normalize() # the triangulation!
    centGraph = createCentroidGraph(triPoints, hullPts)
    startPoint = (0,0)
    endPoint = (img.shape[1], img.shape[0])
    startCent = closestCent(centroids, startPoint)
    endCent = closestCent(centroids, endPoint)

    # Use Djikstras Algorithm on our Networkx Centroid Graph
    shortestPath = nx.dijkstra_path(centGraph, startCent, endCent, weight = 'weight')
    shortPathCoords = [centroids[n] for n in shortestPath]
    return shortPathCoords

# This part displays the classroom polygon with holes and saves it as "img_hole.png"
axes = plt.gca()
ext = [(0, 0), (0, newImage.shape[0]), (newImage.shape[1], newImage.shape[0]), (newImage.shape[1], 0)]
inter = hulls
points, actions = makePathFriendly(ext, inter)
path = Path(points, actions)
patch = PathPatch(path)
axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])
axes.add_patch(patch)
plt.savefig("path_progression/img_hole.png")

# makes polygon of classroom with hulls as holes
points = shapely.Polygon([(0, 0), (0, newImage.shape[0]), (newImage.shape[1], newImage.shape[0]), (newImage.shape[1], 0)], holes=hulls)
triPoints = shapely.constrained_delaunay_triangles(points).normalize() # the triangulation!
triPtsList = formatPolyPts(triPoints)

# This part displays the TRIANGULATION of the classroom polygon with holes and saves it as "img_triangulation.png"
for coords in triPtsList: # iterates through triangles in triangulation
    pathCoords = coords.copy()
    pathCoords.append((0, 0))
    path = Path(pathCoords, [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    patch = PathPatch(path)
    axes.add_patch(patch)
axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])

plt.savefig("path_progression/img_triangulate.png")

# This part adds the centroids to the triangulated classroom
centroids = makeCentroids(triPoints)

xs = [c[0] for c in centroids]
ys = [c[1] for c in centroids]
axes.scatter(xs,ys, color = 'pink', s=10)
axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])
plt.savefig("path_progression/img_holes_cent.png")

centroid_Graph = createCentroidGraph(triPoints, hulls)
centroids = makeCentroids(triPoints)

for node in centroid_Graph:
    x1,y1 = centroids[node]
    for neighbor, i in centroid_Graph[node].items():
        x2,y2 = centroids[neighbor]
        axes.plot([x1,x2],[y1,y2], color = 'lightgray')

axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])
plt.savefig("path_progression/img_holes_graph.png")

# Finding the closest centroid to the starting and end point for the robot
startPoint = (0,0)
endPoint = (newImage.shape[1], newImage.shape[0])

startCent = closestCent(centroids, startPoint)
endCent = closestCent(centroids, endPoint)

# Use Djikstras Algorithm on our Networkx Centroid Graph
shortestPath = nx.dijkstra_path(centroid_Graph, startCent, endCent, weight = 'weight')

shortPathCoords = [centroids[n] for n in shortestPath]
shortPathX = [p[0] for p in shortPathCoords]
shortPathY = [p[1] for p in shortPathCoords]

axes.plot(shortPathX, shortPathY, color = 'red')
axes.scatter(shortPathX, shortPathY, color ='red', s=10)
plt.savefig("path_progression/shortestPathGraph.png")
plt.close("all")