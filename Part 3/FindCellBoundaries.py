# In order to run the code use the following Command in Command prompt:
# python3 part3.py --image data/im#.jpg --mask data/im#_mask.jpg



# Importing necessary packages and libraries

import cv2
import numpy as np
import argparse
from skimage.feature import peak_local_max



# Parsing Image and obtained Mask (from Step 1) using Command Line:
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-m", "--mask", required=True)
ap.add_argument("-t", "--text")
args = vars(ap.parse_args())


# Applying Mask to the Image and blurring it:
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mask = cv2.imread(args["mask"])[:,:,0]
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

dist = cv2.distanceTransform(cell_images, cv2.DIST_L2, 5)

distNorm = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)


localMaxes = peak_local_max(dist, min_distance=5, indices=True, exclude_border=False)
for i in localMaxes:
    cv2.circle(dist, tuple(i[::-1]), 1, 255, -1)
regional_maxima = np.zeros_like(dist, dtype="uint8")
threshold = 0.1 * np.max(dist)
regional_maxima[np.where(dist > threshold)] = 255






dist = np.round(dist * 255).astype(np.uint8)



def get_8_connected_component(x, y, shape):
    out = []
    maxx = shape[1] - 1
    maxy = shape[0] - 1

    # top left
    outx = min(max(x - 1, 0), maxx)
    outy = min(max(y - 1, 0), maxy)
    out.append((outx, outy))

    # top center
    outx = x
    outy = min(max(y - 1, 0), maxy)
    out.append((outx, outy))

    # top right
    outx = min(max(x + 1, 0), maxx)
    outy = min(max(y - 1, 0), maxy)
    out.append((outx, outy))

    # left
    outx = min(max(x - 1, 0), maxx)
    outy = y
    out.append((outx, outy))

    # right
    outx = min(max(x + 1, 0), maxx)
    outy = y
    out.append((outx, outy))

    # bottom left
    outx = min(max(x - 1, 0), maxx)
    outy = min(max(y + 1, 0), maxy)
    out.append((outx, outy))

    # bottom center
    outx = x
    outy = min(max(y + 1, 0), maxy)
    out.append((outx, outy))

    # bottom right
    outx = min(max(x + 1, 0), maxx)
    outy = min(max(y + 1, 0), maxy)
    out.append((outx, outy))
    return out

outimg = np.zeros(dist.shape, dtype="uint8")


outimg = np.zeros(dist.shape, dtype="uint8")
for localMax in localMaxes:
    seed_points = []
    seed_points.append((localMax[0], localMax[1]))
    processed = []
    while (len(seed_points) > 0):
        pix = seed_points[0]
        print(pix)
        outimg[pix[0], pix[1]] = 255
        # if localMax[0] >= pix[1] and localMax[1] >= pix[0]:
        #     break
        for coord in get_8_connected_component(pix[0], pix[1], dist.shape):
            if dist[coord[0], coord[1]] != 0:
                outimg[coord[0], coord[1]] = 255
                if not coord in processed:
                    seed_points.append(coord)
                processed.append(coord)
        seed_points.pop(0)


cv2.imshow('Region Growing', outimg)
cv2.waitKey(0)
cv2.destroyAllWindows()







