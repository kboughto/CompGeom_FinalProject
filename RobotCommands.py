import ConvexHullTakeTwo as Conv
import PolygonBreakdown as Poly

img = Conv.getImage()
img_contours, img_hier = Conv.prepImage(img)
hulls = Conv.makeConvexHulls(img_contours, img_hier, img)

shortestCoords = Poly.getShortestPathCoords(hulls, img)
print(shortestCoords)