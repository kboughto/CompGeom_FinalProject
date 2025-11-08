"""This module tries making Convex Hulls around images using the Canny Edge Detection technique:
basically turning an image into a binary one by making pixels with dratic color change one color and every other pixel another.
The issue with this is these edges are too precise and don't make closed shapes. I was hoping using a Convex Hull
would close it up, but that's not proving to be the case.
Code was used from https://learnopencv.com/edge-detection-using-opencv/"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def getHullPoints():
    reformatHulls = []

    return hull

# makes Convex Hull given the contours (an array of coordinate points)
def makeConvexHull(contours, img, hullPoints):
    # calculate points for each contour
    imgArea = img.shape[0] * img.shape[1]
    for i in range(len(contours)):
        # creating convex hull object for each contour
        # print("Area percentage at ", i, ": ", cv2.contourArea(contours[i])/imgArea)
        if cv2.contourArea(contours[i])/imgArea < 0.05: # hulls must be smaller than 5%
            hullPoints.append(cv2.convexHull(contours[i], False))

    img_hull = img.copy()
 
    # draw contours and hull points
    for i in range(len(hullPoints)):
        color = (255, 0, 0) # red - color for convex hull
        # draw ith convex hull object
        cv2.drawContours(img_hull, hullPoints, i, color, 1, 8)
        # cv2.fillConvexPoly(img_hull, hull[i], color)
        
    return img_hull

# img = cv2.imread("empty_classroom.jpg")
img = cv2.imread("house_living_room.jpg")
hull = []

img_invert = cv2.bitwise_not(img)
img_blur = cv2.blur(img_invert, (int(25/1111 * img.shape[0]), int(25/1500 * img.shape[1]))) # blurs the image

img_edges = cv2.Canny(image=img_blur, threshold1=20, threshold2=40) # Canny Edge Detection. Works SHOCKINGLY well
img_blur_edges = cv2.blur(img_edges, (int(15/1111 * img.shape[0]), int(15/1500 * img.shape[1]))) # blurs the image

# from the threshold image, it finds the contours of it
contours, hierarchy = cv2.findContours(img_blur_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img_hull = makeConvexHull(contours, img, hull)

# plt.figure(figsize=(12, 5))

# plt.subplot(1, 2, 1)
# plt.imshow(img)
# plt.title("Original Image")
# plt.axis("off")

# # plt.subplot(1, 2, 2)
# # plt.imshow(img_blur_edges)
# # plt.title("Canny Edge Image")
# # plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(img_hull)
# plt.title("Hulled Image")
# plt.axis("off")

# plt.tight_layout()
# plt.show()