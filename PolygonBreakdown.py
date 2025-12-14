"""
Authors: Keshawn Boughton & Nadezhda Dominguez Salinas

This file takes in an image of a classroom environment, detects the obstacle polygons within it, constructs the 
constrained Delaunay triangulation of area excluding obstacles, constructs the centroid graph, and 
finds the shortest path between two points (centroids) avoiding obstacles, using Dijkstra's.
It utilizes the convex hulls made in the ConvexHullTakeTwo.py file, for the obstacle polygons.

Code documentation used for triangulation used from: https://shapely.readthedocs.io/en/2.1.2/reference/shapely.constrained_delaunay_triangles.html
Code documentation for parts of the visualization used from https://stackoverflow.com/questions/8919719/how-to-plot-a-complex-polygon
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

def formatPolyPts(polyTri):
    """
    Converts a Shapely geomtry object of triangles into coordinate lists.

    Parameters:
    polyTri : shapely.geomtry.GeomtryCollection
    A collection of triangular polygons producted by a constrained Delunay Triangulation.
    
    Returns:
    list[list[tuple[float,float]]]
    A list in which each element is a list of (x,y) coordinate typles which represent the exterior
    vertices of a triangle. 
    """
    polyPts = []
    for i in range(len(polyTri.geoms)):
        polyPts.append([])
        x, y = polyTri.geoms[i].exterior.xy
        for j in range(len(x)-1):
            polyPts[i].append((x[j], y[j]))
    return polyPts

def makePathFriendly(extPts, interPts):
    """
    Formats polygon boundary and hole coordinates for Matplotlib Path plotting.
    This fuction converts the exterior and interior polygon coordinates into a vertex list and corresponding
    Path action list compatible with the matplotlib.path.Path plotting.

    Parameters:
    extPts: list[tuple[float,float]]
    This is an ordered list of (x,y) coordinates defining the exterior boundary of the polygon.
    
    interiorPts: list[list[tuple[float,float]]]
    This is a list of polygons, where each polygon is represented by a list of (x,y) coordinates which represent
    an interior hole.

    Returns:
    tuple[list[tuple[float,float]], list[int]]
    This is a tuple which contains a list of vertices, and a list of Path action format to use for plotting.
    """
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

def createCentroidGraph(triangles, hullPts):
    """
    Builds a centroid navigation graph from the CDT. In which each triangle centroid is a node in a networkx graph.
    Then, edges are constructed between the centroids of adjacent triangles if the connection between nodes 
    does not interest any of the obstacle boundaries.

    Parameters:
    triangles: shapely.geomtry.GeomtryCollection
    This is a collectino of triangles from the contrained Delaunay triangulation of the free space in class.

    hullPts: list[list[tuple[float,float]]]
    This is a list of obstacles hulls, in which each hull is represented a as a list of (x,y) coordinate tuples.

    Returns:
    A networkx.Graph which is an undirected weighed graph in which the nodes are triangle centroids of CDT and
    the edge weights are the Euclidean distances in between the centroids.
    """
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

def makeCentroids(triPts):
    """
    Computes the centroids for the collection of triangles from the CDT.

    Parameters:
    triPts: shapely.geomtry.GeomtryCollection
    This is the collection of triangule polygons from the CDT found of an environment.

    Returns:
    list[tuple[float,float]]
    This is a list of (x,y) coordinate tuples which are the centroids of each triangle from the CDT
    """
    centroidsCDT = []
    for tri in triPts.geoms:
        cent = shapely.centroid(tri)
        centroidsCDT.append((cent.x, cent.y))
    return centroidsCDT

def lineIntersectsPoly(line, polyCoords):
    """
    Checks whether a given line segment intersects the boundary of an obstacle polygon.

    Parameters:
    line: shapely.geomtry.LineString
    This is the line segment that will be checked to see if intersection occured.

    polyCoords: list[list[tuple[float,float]]]
    This is the list of obstacle polygons, where each is represented as a list of (x,y) coordinate tuples.

    Returns:
    boolean, where True indicates the line intersected a obstacle boundary, otherwise it returns False.
    """
    for hull in polyCoords:
        hulPoly = shapely.Polygon(hull)
        if hulPoly.boundary.intersects(line):
            return True
    return False

def closestCent(centroids, point):
    """
    Finds the index of the centroid which is closest to the specificed point.

    Parameters:
    centroid : list[tuple[float,float]]
    The list of centroid coordinates.

    point: tuple[float,float]
    The (x,y) coordinate of the point being specified.

    Returns:
    int: which is the index of the centroid that is closest in distance to the point.
    """
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
    """
    Computes the shortest path throughout the environment avoiding obstacle polygons.
    This functions first constructs the constrained Delaunay triangulation of the classroom environmet. 
    Then it builds the centroid graph, and uses Dijkstra's algorithm to compute the shortest path from the
    start point (centroid) to the goal point (centroid).

    Parameters:
    hullPts: list[list[tuple[float,float]]]
    The list of obstacle hull polygons represented as coordinate tuples.

    img: numpy.ndarray
    This is the image array that is used for the classroom environment dimensions 

    Returns:
    list[tuple[float,float]]
    This is the ordered list of centroid coordinates from the shortest path of the two points.
    """
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
plt.savefig("path_progression/classroom_setup.png")

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

plt.savefig("path_progression/constrained_delaunay_triangulation.png")

# This part adds the centroids to the triangulated classroom
centroids = makeCentroids(triPoints)

xs = [c[0] for c in centroids]
ys = [c[1] for c in centroids]
axes.scatter(xs,ys, color = 'pink', s=10)
axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])
plt.savefig("path_progression/centroids_CDT.png")

centroid_Graph = createCentroidGraph(triPoints, hulls)
centroids = makeCentroids(triPoints)

for node in centroid_Graph:
    x1,y1 = centroids[node]
    for neighbor, i in centroid_Graph[node].items():
        x2,y2 = centroids[neighbor]
        axes.plot([x1,x2],[y1,y2], color = 'lightgray')

axes.set_xlim(0,newImage.shape[1])
axes.set_ylim(0,newImage.shape[0])
plt.savefig("path_progression/centroid_graph.png")

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
plt.savefig("path_progression/shortest_path_graph.png")
plt.close("all")