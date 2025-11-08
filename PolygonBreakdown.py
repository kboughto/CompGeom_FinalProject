"""This attempts to first plot a rectangle of the dimensions of a given image with 'holes'
made from the convex hulls made in ConvexHullTakeTwo"""

from shapely import Polygon
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import ConvexHullTakeTwo as imgConv

newImage = cv2.imread("house_living_room.jpg")

formatHulls = []
formatHullsx = []
formatHullsy = []
hulls = imgConv.getHullPoints()
for evenBracketedcoords in hulls[0]:
    for brackedCoords in evenBracketedcoords:
        formatHullsx.append(int(brackedCoords[0]))
        formatHullsy.append(int(brackedCoords[1]))
        formatHullsy.append((int(brackedCoords[0]), int(brackedCoords[1])))

def makeShapeFromImage(img, holes=None):
    imgShape = Polygon(((0, 0), (img.shape[0], 0), (img.shape[0], img.shape[1]), (0, img.shape[1])), holes=holes)
    return imgShape


newPolygon = makeShapeFromImage(newImage, [formatHulls])
outx = [0, newImage.shape[0], newImage.shape[0], 0]
outy = [0, 0, newImage.shape[1], newImage.shape[1]]
inx = formatHullsx
iny = formatHullsy
plt.fill(outx+inx, outy+iny, color="blue")
plt.show()