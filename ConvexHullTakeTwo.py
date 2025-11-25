"""This module tries making Convex Hulls around images using the Canny Edge Detection technique:
basically turning an image into a binary one by making pixels with dratic color change one color and every other pixel another.
Code was used from https://learnopencv.com/edge-detection-using-opencv/"""

import cv2
import matplotlib.pyplot as plt

# Initializes variables
img = cv2.imread("sample_classrooms/circle_classroom.png")
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

# Returns the Hull Points formatted as a dictionary whose
# keys are the indices of Convex Hulls and the
# values are the corresponding coordinates
def getHullPoints(ptsFile):
    reformatHulls = {}
    for i in range(len(hull)):
        reformatHulls[i] = []
        ptsFile.write("Hull #" + str(i) + ": \n")
        for bracketedCoords in hull[i]:
            for actualCoords in bracketedCoords:
                reformatHulls[i].append((int(actualCoords[0]), int(actualCoords[1])))
                ptsFile.write(str(actualCoords[0]) + "," + str(actualCoords[1]) + "\n")
        ptsFile.write("\n")
    return reformatHulls

def getImage():
    return img

def prepImage(img, hullFile):
    hullFile.write("Image coordinates:\n")
    hullFile.write("0,0\n0," + str(img.shape[0]) + "\n" + str(img.shape[0]) + "," + str(img.shape[1]) + "\n" + str(img.shape[1]) + ",0\n\n")

    img_invert = cv2.bitwise_not(img) # turns every pixel of image into its negative. More likely to darken image, which makes edges more apparent
    img_blur = cv2.blur(img_invert, (int(25/1111 * img.shape[0]), int(25/1500 * img.shape[1]))) # blurs the image. Done to make detected edges surround more obvious features of image

    img_edges = cv2.Canny(image=img_blur, threshold1=20, threshold2=40) # Canny Edge Detection. Works SHOCKINGLY well with detecting objects
    img_blur_edges = cv2.blur(img_edges, (int(15/1111 * img.shape[0]), int(15/1500 * img.shape[1]))) # blurs the image AGAIN so Convex Hulls surround most obvious objects

    contours, hierarchy = cv2.findContours(img_blur_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # makes coordinates of Convex Hulls in the form of an array of array of coordinates
    # NOTE: "hierarchy" is a list of arrays that correspond to the indices of Convex Hull points such that for each index i in contours list:
    # - hierarchy[0][i][0] presents contour directly NEXT to contours[i]
    # - hierarchy[0][i][1] presents contour directly PREVIOUS to contours[i]
    # - hierarchy[0][i][2] presents first child of contour[i], i.e. first contour inside contour[i]
    # - hierarchy[0][i][3] presents parent of contour[i], i.e. immediate contour surrounding contour[i]
    
    return contours, hierarchy

def drawContoursOntoImage(img, hullPts): 
    # draw contours and hull points
    for i in range(len(hullPts)):
        color = (255, 0, 0) # red - color for convex hull
        # draw ith convex hull object
        cv2.drawContours(img, hullPts, i, color, 2, 8)

# Given an image, contours from the image's edges and an empty list, 
# polygons approximately cover significant objects on the image.
# Returns that edited image
def makeConvexHulls(contours, hierarchy, img, hullPoints):
    imgArea = img.shape[0] * img.shape[1] # area of original image
    hullIndices = []
    for i in range(len(contours)):
        # creating convex hull object for each contour
        if cv2.contourArea(contours[i])/imgArea < 0.05: # hulls must be smaller than 5% of the image
            hullIndices.append(i) # keeps track of indices of legal Convex Hulls in contours
            hullPoints.append(cv2.convexHull(contours[i], False))

    hierMap = makeHierMap(hullIndices, hierarchy)
    hullLenDict = {}
    for hier in hierMap.keys():
        hullLenDict[len(hierMap[hier])] = hier
    
    hullPoints = [hullPoints[ind] for ind in hierMap[hullLenDict[min(hullLenDict.keys())]]] # captures all Convex Hull points from the hierarchy tier with the least # of hulls
        
    return hullPoints

ConvFile = open("ConvexHullPoints.txt", "w")
img_contours, img_hier = prepImage(img, ConvFile)
hull = makeConvexHulls(img_contours, img_hier, img, hull)
getHullPoints(ConvFile)

# plt.figure(figsize=(12, 5))

# plt.subplot(1, 2, 1)
# plt.imshow(img)
# plt.title("Original Image")
# plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(img_blur_edges)
# plt.title("Canny Edge Image")
# plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(img_hull)
# plt.title("Hulled Image")
# plt.axis("off")

# plt.tight_layout()
# plt.show()