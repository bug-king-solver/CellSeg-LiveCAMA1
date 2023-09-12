# CellSeg-LiveCAMA1

This is an algorithm for detecting and segmenting cells in live cell images of the CAMA-1 cell line.

### Introduction:

The aim of this project is to obtain a foreground mask of cells, then finding the cell locations for detecting the cell boundaries and segmenting cells in live cell images. Three different cell images are provided in this assignment. Also, a .txt ground truth foreground mask file is provided for all three images to assess the precision, recall, and F1-score metrics for our obtained mask. Aiming to do so, we used Scikit-image and OpenCV libraries in Python programming language to read and process each image. For each part of assignment, there are different steps are followed for segmenting the images at the end. We will explain them in following sections.

# **Part 1**

The task is to obtain a foreground mask for an RGB image, where foreground pixels are labeled with 1 and background pixels with 0. The provided code implements a method to achieve this task. In this report, we will present a detailed explanation of the implemented method, the selection of its parameters, visual results for the provided images, and quantitative metrics to evaluate the performance.

### Method:

The provided code implements the following method to obtain a foreground mask:

- Load the image and convert it to grayscale.
- Apply Gaussian blur to reduce noise in the image.
- Threshold the image using a threshold value of 170 and invert the binary image.
- Find the contours of the foreground objects in the binary image.
- Fill the holes in the binary image.
- Compare the obtained mask with the ground truth mask to calculate precision, recall, and F-score.

### Parameters:

The method takes one input, the path of the RGB image, and one optional parameter, the path of the ground truth mask. The parameter for Gaussian blur is (11,11), and the threshold value is 170. The default settings are used for filling the holes in the binary image. The parameters for finding contours are cv2.RETR_CCOMP and cv2.CHAIN_APPROX_SIMPLE.

### Parameter Selection:

The value of the threshold is selected by trial and error. The value of 170 was found to work well for the provided images. The kernel size for Gaussian blur is selected as (11,11), which is a commonly used value for removing noise in images. The default settings for filling the holes in the binary image are used as they work well in most cases. The parameters for finding contours are selected based on their suitability for detecting contours with holes, which is common in natural images.

### Visual Results:

The provided code is tested on three images, and the obtained masks are visualized alongside the ground truth masks. The images and masks are shown in Table 1. As can be seen from the figure, the obtained masks closely match the ground truth masks.

![Table 1](https://user-images.githubusercontent.com/132440248/251685496-84a6ce9e-5794-4f83-a2af-fbf4546ca4dd.png)

### Quantitative Metrics:

The quantitative metrics for evaluating the performance of the method are precision, recall, and F-score. The results for the three images are presented in Table 2. As can be seen from the table, the method performs well on all three images, with F-scores above 0.9 for all images.

<p align="center">
<img src="https://user-images.githubusercontent.com/132440248/251686103-ea5b5662-c7cd-4bd2-ad4e-445211e45bea.png" width="450" height="130">
</p>

# **Part 2**

In the second part of the assignment, we need to find the approximate location of each cell by using distance transforms. The distance transform is an operator normally only applied to binary images. The result of the transform is a gray level image that looks similar to the input image, except that the gray level intensities of points inside foreground regions are changed to show the distance to the closest boundary from each point. For example, when a distance transform is applied scaled by a factor of 3 it can be like the following images:

<p align="center">
  <img src="https://user-images.githubusercontent.com/132440248/251687633-d90b675a-1e9a-4cb7-a3ec-3aef730bc754.png" width="250" height="80">
</p>

So for doing this, we implement the code in the method section:

### Method:

The provided code implements the following method to find the cell locations:

- Load the image and obtained mask.
- Applying Mask to the Image and blurring it.
- Performed image enhancement technique (CLAHE) on blurred masked image and binarized it.
- Apply morphological operations on the masked image and convert it to the binary image.
- Perform the distance transform algorithm and normalization.
- Find the local maxima related to each cell and save the XY coordinates as a CSV file.
- Finally calculate true positives, false positives, and false negatives for each cell.

### Parameters:

The method takes two inputs, RGB image and the obtained mask. The parameter for Median filter is 7, and the clipLimit and tileGridSize parameters values for CLAHE are 15 and (30,30) respectively. The threshold value is 150 which performed better is comparison with higher values. For the distance transform function, it calculates the distance of each pixel from the nearest non-zero pixel. This function takes in three arguments: the binary image, the distance type (which is cv2.DIST_L2 for Euclidean distance), and the mask size (which is 3 for a 3×3 mask). The default settings are used for normalization.

### Visual Results:

The provided code is tested on three images, and the distance transform and obtained cell locations are visualized for each image. The images are shown in Table 3.

<p align="center">
  <img src="https://user-images.githubusercontent.com/132440248/251695267-5851bc56-eb51-4b9c-b27f-1bac16e1bb7a.png">
</p>

### Quantitative Metrics:

The quantitative metrics for evaluating the performance of the method are precision, recall, and F-score. The results for the three images are presented in Table 4.

<p align="center">
  <img src="https://user-images.githubusercontent.com/132440248/251695916-8a4fe22f-87c0-41e0-a350-0954e95da4d5.png" width="450" height="130">
</p>

# **Part 3**

### Introduction:

In this task, the objective is to implement an algorithm for finding cell boundaries. This algorithm takes an RGB image, an estimated foreground map, and an estimated set of cell locations as inputs. To achieve this, a region growing algorithm is used with the estimated set of cell locations as initial seeds. The results should be evaluated using cell-level Dice index and intersection-over-union metrics for thresholds of 0.5, 0.75, and 0.9, using a gold standard provided in a file called im\*\_gold_cells.txt. It is important to match the estimated cells with the gold standard cells based on their overlapping pixels rather than their ids.

### Method:

In this task we performed the region growing method. The description is mentioned below step by step from the second task to this task:

- Applying the mask to the image and blurring it.
- Using Contrast Limited Adaptive Histogram Equalization (CLAHE) to enhance the image.
- Applying thresholding on the enhanced image and applying the mask.
- Performing Morphological Operations on the masked image.
- Converting the masked image to a binary image.
- Applying the distance transform to the binary image.
- Normalizing the distance transform.
- Finding the local maxima in the distance transform.
- Using region growing to segment the image based on the local maxima.
- Displaying the segmented image.

For this task we implemented a function. This function get_connected_component(x, y, shape) returns a list of 8-connected neighbors of a pixel in an image. The function first initializes an empty list called out, which will store the coordinates of the 8-connected neighbors. It then computes the indices of the neighboring pixels in the horizontal and vertical directions using simple arithmetic on x and y. For example, to get the top-left neighbor, it subtracts 1 from both x and y and takes the minimum of each with the maximum possible index value in that direction (i.e., 0 for the top-left corner and the shape of the image minus 1 for the bottom-right corner). The function appends the resulting (x, y) tuple to the out list. The function repeats this process for each of the 8 neighbors, and then returns the out list of neighboring pixel coordinates.

### Visual results:

<p align="center">
  <img src="https://user-images.githubusercontent.com/132440248/251697161-0f81d5e6-42e1-4c55-b6e1-248f44d10baf.png">
</p>
