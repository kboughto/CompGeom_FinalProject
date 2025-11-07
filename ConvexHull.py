import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

"""This module tries making Convex Hulls around images using thresholding:
basically turning an image into a binary one by making pixels bayond a certain hue white and every other pice black.
The issue with this is most house objects are very similar colors to its surroundings.
Code was used from https://learnopencv.com/convex-hull-using-opencv-in-python-and-c/"""

img = cv2.imread("house_living_room.jpg")

img_invert = cv2.bitwise_not(img)
img_blur = cv2.blur(img_invert, (10, 10)) # blurs the image

colorThres = 75
# makes a new image which turns pixels black if they're any lighter than 150 and white otherwise
ret, img_thresh = cv2.threshold(img_blur, colorThres, 255, cv2.THRESH_BINARY)
img_gray = cv2.cvtColor(img_thresh, cv2.COLOR_BGR2GRAY) # processes image in grayscale

# from the threshold image, it finds the contours of it
contours, hierarchy = cv2.findContours(img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# create hull array for convex hull points
hull = []
 
# calculate points for each contour
for i in range(len(contours)):
    # creating convex hull object for each contour
    hull.append(cv2.convexHull(contours[i], False))

# create an empty black image
img_hull = np.zeros((img_thresh.shape[0], img_thresh.shape[1], 3), np.uint8)
 
# draw contours and hull points
for i in range(len(contours)):
    color_contours = (0, 255, 0) # green - color for contours
    color = (255, 0, 0) # blue - color for convex hull
    # draw ith contour
    cv2.drawContours(img_hull, contours, i, color_contours, 1, 8, hierarchy)
    # draw ith convex hull object
    cv2.drawContours(img_hull, hull, i, color, 1, 8)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img_invert)
plt.title("Inverted Image")
plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(img_gray)
# plt.title("Threshold Image")
# plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(img_hull)
plt.title("Hulled Image")
plt.axis("off")

plt.tight_layout()
plt.show()
