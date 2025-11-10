"""This module tries making Convex Hulls around images using the Canny Edge Detection technique:
basically turning an image into a binary one by making pixels with dratic color change one color and every other pixel another.
Code was used from https://learnopencv.com/edge-detection-using-opencv/"""

import cv2
import matplotlib.pyplot as plt

# Initializes variables
img = cv2.imread("circle_classroom.png")
hull = []

# Given a contour in the form of a hierarchy array and the list of hierarchy arrays,
# it determines the hierarchy of the contour
def getHierarchy(contour, hierarchy):
    hier = 1
    nextParent = contour[3]
    while nextParent != -1:
        nextParent = hierarchy[0][nextParent][3]
        hier += 1
    return hier

# makes a hashmap (as Python calls it, a dictionary) where the keys are the possible hierarchies
# of Convex Hulls and the values are the indices of the Hull points which are in that hierarchy.
# Returns the hashmap
def makeHierMap(hullIndices, hierarchy):
    hierMap = {}
    for i in range(len(hullIndices)):
        hier = getHierarchy(hierarchy[0][hullIndices[i]], hierarchy)
        if hierMap.keys().__contains__(hier):
            hierMap[hier].append(i)
        else:
            hierMap[hier] = []
            hierMap[hier].append(i)
    return hierMap

# Returns the Hull Points formatted as a list containing a list of tuples of coordinate points
def getHullPoints():
    reformatHulls = []
    # for i in range(len(hull)):
    return reformatHulls

def getImage():
    return img

# Given an image, contours from the image's edges and an empty list, 
# polygons approximately cover significant objects on the image.
# Returns that edited image
def makeConvexHull(contours, hierarchy, img, hullPoints):
    # calculate points for each contour
    imgArea = img.shape[0] * img.shape[1]
    hullIndices = []
    for i in range(len(contours)):
        # creating convex hull object for each contour
        if cv2.contourArea(contours[i])/imgArea < 0.05: # hulls must be smaller than 5% of the image
            hullIndices.append(i)
            hullPoints.append(cv2.convexHull(contours[i], False))

    hierMap = makeHierMap(hullIndices, hierarchy)
    hullLenDict = {}
    for hier in hierMap.keys():
        hullLenDict[len(hierMap[hier])] = hier
    
    hullPoints = [hullPoints[ind] for ind in hierMap[hullLenDict[min(hullLenDict.keys())]]]

    img_hull = img.copy()
 
    # draw contours and hull points
    for i in range(len(hullPoints)):
        color = (255, 0, 0) # red - color for convex hull
        # draw ith convex hull object
        cv2.drawContours(img_hull, hullPoints, i, color, 1, 8)
        # cv2.fillConvexPoly(img_hull, hull[i], color)
        
    return img_hull

img_invert = cv2.bitwise_not(img)
img_blur = cv2.blur(img_invert, (int(25/1111 * img.shape[0]), int(25/1500 * img.shape[1]))) # blurs the image

img_edges = cv2.Canny(image=img_blur, threshold1=20, threshold2=40) # Canny Edge Detection. Works SHOCKINGLY well
img_blur_edges = cv2.blur(img_edges, (int(15/1111 * img.shape[0]), int(15/1500 * img.shape[1]))) # blurs the image

# from the threshold image, it finds the contours of it
contours, hierarchy = cv2.findContours(img_blur_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_hull = makeConvexHull(contours, hierarchy, img, hull)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Image")
plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(img_blur_edges)
# plt.title("Canny Edge Image")
# plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(img_hull)
plt.title("Hulled Image")
plt.axis("off")

plt.tight_layout()
plt.show()