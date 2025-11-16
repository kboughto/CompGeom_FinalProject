"""This attempts to first plot a rectangle of the dimensions of a given image with 'holes'
made from the convex hulls made in ConvexHullTakeTwo.
Code might be used from https://stackoverflow.com/questions/8919719/how-to-plot-a-complex-polygon"""

import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import ConvexHullTakeTwo as imgConv

newImage = imgConv.getImage()
print(newImage.shape)

formatHullsx = []
formatHullsy = []
formatHulls = []
hulls = imgConv.getHullPoints()
for evenBracketedcoords in hulls[0]:
    for brackedCoords in evenBracketedcoords:
        formatHullsx.append(int(brackedCoords[0]))
        formatHullsy.append(int(brackedCoords[1]))
        formatHulls.append((int(brackedCoords[0]), int(brackedCoords[1])))

def makeShapeFromImage(img):
    axes = plt.gca()
    imgShape = Path([(0, 0), (img.shape[0], 0), (img.shape[0], img.shape[1]), (0, img.shape[1])])
    patch = PathPatch(imgShape)
    axes.add_patch(patch)
    return axes


makeShapeFromImage(newImage)
# outx = [0, newImage.shape[0], newImage.shape[0], 0]
# outy = [0, 0, newImage.shape[1], newImage.shape[1]]
# inx = formatHullsx
# iny = formatHullsy
plt.show()