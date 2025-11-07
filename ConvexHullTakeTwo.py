import cv2
import matplotlib.pyplot as plt
import numpy as np

"""This module tries making Convex Hulls around images using the Canny Edge Detection technique:
basically turning an image into a binary one by making pixels with dratic color change one color and every other pixel another.
The issue with this is these edges are too precise and don't make closed shapes. I was hoping using a Convex Hull
would close it up, but that's not proving to be the case"""

img = cv2.imread("house_living_room2.jpg")

img_invert = cv2.bitwise_not(img)
img_blur = cv2.blur(img_invert, (15, 15)) # blurs the image

img_edges = cv2.Canny(image=img_blur, threshold1=20, threshold2=40) # Canny Edge Detection. Works SHOCKINGLY well
# norm_edges = cv2.normalize(img_edges, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
# norm_edges = norm_edges.astype(np.uint8)
# img_edges_gray = cv2.cvtColor(norm_edges, cv2.COLOR_BGR2GRAY) # processes image in grayscale

# # from the threshold image, it finds the contours of it
# contours, hierarchy = cv2.findContours(img_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # create hull array for convex hull points
# hull = []
 
# # calculate points for each contour
# for i in range(len(contours)):
#     # creating convex hull object for each contour
#     hull.append(cv2.convexHull(contours[i], False))

# # create an empty black image
# img_hull = np.zeros((img_edges.shape[0], img_edges.shape[1], 3), np.uint8)
 
# # draw contours and hull points
# for i in range(len(contours)):
#     color_contours = (0, 255, 0) # green - color for contours
#     color = (255, 0, 0) # blue - color for convex hull
#     # draw ith contour
#     cv2.drawContours(img_hull, contours, i, color_contours, 1, 8, hierarchy)
#     # draw ith convex hull object
#     cv2.drawContours(img_hull, hull, i, color, 1, 8)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(img_edges)
plt.title("Canny Edge Image")
plt.axis("off")

plt.tight_layout()
plt.show()