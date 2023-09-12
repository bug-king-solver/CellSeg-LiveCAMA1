In this task, we will design an algorithm for detecting and segmenting cells in live cell images of the CAMA-1 cell line. 
We will work on the three images that are provided for this task. For each image, there are three files:

- ***im#.jpg:*** RGB image file
- ***im#_gold_cells.txt:*** Text file containing cell label annotations. In this file, cells are labeled from 1 to N, where N is the number of 
    cells. All pixels of the same cell are labeled with the same ID. Background pixels are labeled as 0.
- ***im#_gold_mask.txt:*** Text file containing a rough mask for foreground (cell) pixels.
    In this file, foreground pixels are labeled with 1 and background pixels with 0.

Below is an example of such an image, its annotated cells, and its mask. Note that annotated pixels of the
same cell are represented with a different color (this coloring is just for illustration, selection of these
colors are random). Also note that these annotations are not perfect and may have some inconsistencies. Please use annotations, as they
are, and do not try to correct them.

![Untitled](https://github.com/AmirTabatabaei-git/CellSeg-LiveCAMA1/assets/132440248/1faaad10-750a-450c-a9e8-a0d5d4995394)


Our algorithm should have the following three steps, each of which we will implement and evaluate:

- **1. ObtainForegroundMask:** <sub> <Part 1 in repository> </sub> It inputs an RGB image and outputs a map of foreground pixels where foreground and background pixels 
    should be labeled with 1 and 0, respectively. 
- **2. FindCellLocations:** <sub> <Part 2 in repository> </sub> It inputs the RGB image and the foreground map, which we will have calculated in the first step, and outputs a set of points (x and y coordinates). Each point will correspond to an approximate location of a cell.
- **3. FindCellBoundaries:** <sub> <Part 3 in repository> </sub> It inputs the RGB image as well as the foreground map and the set of points, which we will have calculated
    in the previous steps, and outputs a segmentation map of cells. In this segmentation map, cells should be labeled from 1 to N. 
    Pixels of the same cell should be labeled with the same ID. Background pixels should be labeled with 0.

Below are the details of requirements we should comply with for implementing each step. As detailed below, we will design an algorithm for
each step. In our design, you may use any techniques available. However, we cannot use any techniques of deep learning. It is important to
note that this task is for us to make a simple design of our own. Thus, although our design should be technically sound, there is no single
“best” answer/design for the task.
In our implementation, we used Python programming language. We may also use the built-in library functions for these techniques (e.g., for filters,
morphology operators, etc.). Obviously, if there is a builtin function for the entire step (e.g., a function for finding the centers when an image 
and a mask are given), we are NOT allowed to use it.

## PART 1: ObtainForegroundMask

This step (algorithm) takes an RGB image as an input. We may use the original RGB image or its grayscale equivalent. We should make our own design, in which we may use thresholding, clustering,
filters, texture analysis, etc. We should consider preprocessing the image and postprocessing the result. We may use filters and/or morphological operators for postprocessing.
After completing its implementation, run this algorithm on the three images that are provided. For each image, compare our estimated foreground mask with the gold standard (stored in a file called
im*_gold_mask.txt). Calculate the pixel-level precision, recall, and F-score metrics.

## PART 2: FindCellLocations

This step (algorithm) takes the RGB image and the estimated foreground map, which is the output of Part 1, as inputs, and outputs a set of points (x and y coordinates), each of which corresponds to an
approximate location of a cell. Our design should be based on the use of distance transforms. However, you may realize that it would not be
possible to identify the regional maxima of the outer distance transform as cell locations in this task. Thus, we should find “a way” to define a more effective distance transform. In this part, we are asked to make
such a definition. Hint: Check the original RGB images. There are very obvious white boundaries in between adjacent cells. In one design possibility, we may identify these boundaries (fully or partially)
and may calculate the distance from each foreground pixel to its closest white boundary.
After defining the distance transform, calculate it for each image and identify the regional maxima of the noise-suppressed distance transform as cells. If necessary, postprocess the resulting regional maxima map to obtain better cell locations. As the requirement of this part, we should decide on
what techniques our design will use for distance transform calculation and postprocessing.
After completing its implementation, run this algorithm on the three images that are provided. For
each image, calculate the cell-level precision, recall, and F-score metrics using the gold standard
(stored in a file called im*_gold_cells.txt). In this calculation, find the number of true positives (TP) as
follows: First calculate the centroid pixel for each regional maximum and match this centroid with the
gold standard cell that it belongs to. (If the centroid is a background pixel in the gold standard, it means
that this centroid corresponds to a false positive.) Afterwards, count the gold standard cells with which
exactly one centroid matches. This gives us the number of TPs.

## PART 3: FindCellBoundaries

This step (algorithm) takes the RGB image, the estimated foreground map, which is the output of Part
1, and the estimated set of cell locations, which is the output of Part 2, as inputs, and estimates a
segmentation map of cells. In this segmentation map, cells should be labeled from 1 to N. Pixels of the
same cell should be labeled with the same id. Background pixels should be labeled with 0. Our design
should be based on the use of a region growing algorithm.
In the design of the region growing algorithm, we should use the estimated set of cell locations as the
initial seeds. However, as the requirement of this part, we should decide the marking function and
the stopping condition of this region growing algorithm.
After completing its implementation, run this algorithm on the three images that are provided. For
each image, calculate the cell-level Dice index and the intersection-over-union metrics for the
thresholds of 0.5, 0.75, and 0.9, using the gold standard (stored in a file called im*_gold_cells.txt).
Here it is important to note that, in the metric calculations, we should match the estimated cells with
the gold standard cells with respect to their overlapping pixels. We should not directly compare the IDs since the estimated IDs might be different that the
IDs given in the gold standard. For example, pixels of an estimated cell with ID=5 may 95 percent
overlap with those of a gold standard cell with ID=35. This is a TP cell even though the IDs are different.
We should make our calculations accordingly.
