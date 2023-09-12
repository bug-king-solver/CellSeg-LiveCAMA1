# Importing necessary packages and libraries

import cv2
import numpy as np
from skimage.feature import peak_local_max


img_path = r"E:\image-HW-1\data\im3.jpg"
mask_path = r"E:\image-HW-1\data\im3_gold_mask.png"

# Applying Mask to the Image and blurring it:
image = cv2.imread(img_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mask = cv2.imread(mask_path)[:,:,0]
masked = cv2.bitwise_and(image,mask, mask=mask)
gray = cv2.medianBlur(masked, 7)


# Using the Contrast Limited Adaptive Histogram Equalization (CLAHE) on blurred masked image
CLAHE = cv2.createCLAHE(clipLimit=15, tileGridSize=(30,30))
CLAHE = CLAHE.apply(gray)


# Applying thresholding on the enhanced image and applying mask
T, thresh = cv2.threshold(CLAHE, 150, 255, cv2.THRESH_BINARY_INV )
mask1 = cv2.bitwise_and(masked, thresh, mask=thresh)


# doing Morphological Operation on the masked image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
opening = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)


# Converting the masked image to Binary image
openBinary = np.zeros_like(opening)
for i in range(0, opening.shape[0]):
    for j in range(0, opening.shape[1]):
        if opening[i][j] != 0:
            openBinary[i][j] = 255


cell_images = cv2.bitwise_and(image, openBinary, mask=openBinary)

# Perform the distance transform algorithm

dist = cv2.distanceTransform(cell_images, cv2.DIST_L2, 3)

# Normalize the distance image for range = {0.0, 1.0}
# so we can visualize and threshold it

dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)

localMax = peak_local_max(dist, min_distance=5, exclude_border=False)
for i in localMax:
    cv2.circle(dist, tuple(i[::-1]), 1, 255, 2)
regional_maxima = np.zeros_like(image, dtype="uint8")
threshold = 0.1 * np.max(dist)
regional_maxima[np.where(dist > threshold)] = 255
print(localMax.shape)


# Save the array as a CSV file
np.savetxt('xy_coordinates.csv', localMax, delimiter=',')


# Load the im*_gold_cells.txt file containing cell label annotations
with open('data\im2_gold_cells.txt', 'r') as f:
    gold_cells = np.loadtxt(f)

# Label the cells in the binary image using connectedComponentsWithStats
num_labels, labeled, stats, centroids = cv2.connectedComponentsWithStats(regional_maxima)


# Initialize variables to calculate precision, recall, and F-score
true_positives = 0
false_positives = 0
false_negatives = 0

# Calculate true positives, false positives, and false negatives for each cell
for i in range(1, num_labels):
    # Find the pixels labeled with cell i in the binary image
    cell_pixels = np.where(labeled == i)

    # Find the label assigned to cell i in the gold standard
    gold_label = np.unique(gold_cells[cell_pixels])[0]

    # If the cell is correctly labeled
    if gold_label != 0 and gold_label == i:
        true_positives += 1
    # If the cell is incorrectly labeled
    elif gold_label == 0:
        false_positives += 1
    elif gold_label != i:
        false_negatives += 1

# Calculate precision, recall, and F-score
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f_score = 2 * (precision * recall) / (precision + recall)

print("Precision:", precision)
print("Recall:", recall)
print("F-score:", f_score)


cv2.namedWindow('main image',cv2.WINDOW_NORMAL)
cv2.namedWindow('Centroids',cv2.WINDOW_NORMAL)
cv2.namedWindow('Distance Transform',cv2.WINDOW_NORMAL)
cv2.imshow('main image', image)
cv2.imshow('Centroids', regional_maxima)
cv2.imshow('Distance Transform', dist)


if cv2.waitKey(0):
    cv2.destroyAllWindows()

