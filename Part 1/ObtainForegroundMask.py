import cv2
import numpy as np

path = r"E:\image-HW-1\data\im3.jpg"
mask_path = r"E:\image-HW-1\data\im3_gold_mask.txt"

img = cv2.imread(path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (11,11), 0)

th, binary = cv2.threshold(blur, 170, 255, cv2.THRESH_BINARY_INV)


des = cv2.bitwise_not(binary)

contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contour:
    cv2.drawContours(des,[cnt],0,255,-1)


from plantcv import plantcv as pcv

pcv.params.debug = "plot"

# Apply fill holes to a binary image

fill_image = pcv.fill_holes(bin_img=des)

mask_data = np.loadtxt(mask_path, dtype=np.uint8)
_, gold_mask = cv2.threshold(mask_data, 0, 255, cv2.THRESH_BINARY)


TP = np.sum(np.logical_and(fill_image, gold_mask))
FP = np.sum(np.logical_and(fill_image, np.logical_not(gold_mask)))
FN = np.sum(np.logical_and(np.logical_not(fill_image), gold_mask))
precision = TP / (TP + FP)
recall = TP / (TP + FN)
f_score = 2 * precision * recall / (precision + recall)


# cv2.imwrite('im*_mask.jpg', fill_image)
print('Image: im3.jpg')
print('Precision:', precision)
print('Recall:', recall)
print('F-score:', f_score)


cv2.namedWindow('main image',cv2.WINDOW_NORMAL)
cv2.namedWindow('ground truth',cv2.WINDOW_NORMAL)
cv2.namedWindow('predicted mask',cv2.WINDOW_NORMAL)
cv2.imshow('main image', img)
cv2.imshow('ground truth', gold_mask)
cv2.imshow('predicted mask', fill_image)

if cv2.waitKey(0):
    cv2.destroyAllWindows()

