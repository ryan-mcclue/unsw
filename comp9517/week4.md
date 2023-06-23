<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Image Segmentation (main problem in computer vision)
NOTE: most used is deep neural networks for segmentation (these techniques used mainly for post-processing)

tangential direction is direction at moment of time

Partition image into meaningful regions, i.e. with labels, e.g. face, hand, etc.
(theoretically could do repeated thresholding...)

Clearly, segmentation easier if regions are uniform/homogenous

In ascending orders of specificity:
1. image classification: assigning image to class, e.g. 'image containing bottle, cup'
2. object localisation: what is in image and where located (a rough rectangular region for each)
3. semantic segmentation: create map that shows every pixel in a class (classes like cube, bottle, etc.)
4. instance segmentation (ultimate goal): type and if unique object, e.g. each cube labelled differently

There is no single segmentation method that works (even in neural networks still overfit for images drastically different from what trained on)

IMPORTANT: as so many techniques, how to evaluate segmentation technique
Thresholding overall not good for overlapping histogram regions (alterations will introduce an have false-positive and false-negatives)

**K-means clustering** good if know how many clusters of objects
If k=3, choose 3 random gray values, for each pixel choose what cluster it's closest to.
Now recompute mean of clusters
Limitation is that need to know k a priori

**Feature Based** create a patch of say size 20x20. 
Iterate over image with patches, and classify (classifier requires many examples for training) features in patches
Expensive, as iterates over all image pixels (a lot of papers about optimisation)

1. Region Splitting and Merging:
* recursive histogram splitting:
  - creation of clusters create masks, i.e. a cluster is a mask
  - then with these new masks run again, until number of clusters converges
* region merging: boundary length, closest/farthest points etc.
  - region dissimilarity determined with MST (so an edge is connects pixel to pixel)
  - merge any two regions whose internal dissimilarity is smaller than the minimum of the internal differences of these two regions
  - could also use region growing based on similarity from seed pixel
* recursively split image into homogenous regions
* simplest way to do this is with thresholding
* then determine connected components. 
  however, number of connected components depends on chosen connectivity, e.g. 4-way or 8-way
Connected Components Labelling Algorithm (from segmented image):
First Pass:
  - for each pixel, check connectivity.
  - if no neighbour label assign, otherwise assign smallest (in the case of smallest, we know these labels are equivalent, i.e. connected)
Second Pass:
  - for each pixel, replace label equivalences with smallest

2. Watershed Segmentation:
  - immersion of surface in water, (building dams and basins?)
Meyer's Flooding Algorithm (priority queue):
 we want regions of interest to have local minima for best results 

3. Maximally Stable Extremal Regions (MSER):
  - iterate over 256 threshold values. for each value, choose the regions whose shape doesn't change

4. Mean Shifting 
(weight function for mean calculation could be Guassian, i.e. give points closer to centre more weight)
each pixel has point in L and U and V, i.e point in 3D space
k-means sensitive to outliers
  - convert image to a point cloud of particular feature space, e.g. could be colour
  - start with a set of seed points
  - calculate mean of region. then move region to that region and repeat until convergence.
  - result is regions that are densest point of point cloud
no need to specify k
robuts to outliers
downside is very computationally expensive. also parameters like window size have to be chosen empirically

5. Super Pixel Segmentation
  - group similar pixels into superpixels (e.g. on colour, texture, etc.)
Simple Linear Iterative Clustering:
  * compute distance of pixel to cluster centre. assign pixel to cluster whose distance smallest
  - segmentation performed on these superpixels to speed up calculations

6. Conditional Random Field
  - create undirected graph, where nodes are superpixels and edges determined by adjacency
  - creating segmentation of superpixels based on minimising energy function. this is solved by max-flow
  - random name as part of energy function computed with probability of pixel matching with a class

7. Active Contour Segmentation
  (snakes algorithm)
  - curve matching
  - start with points. then connect points with interpolated curve. 
  then determine if curve fixed to object, i.e on image boundary via edge detection (see how edges correspond to curve)
  - works well with poor gradient information. typically manual interaction, i.e. define points near where boundary is
    we impose say looking for a circular, ellipitcal solution, etc.

  - TODO: integrate along gradient direction? what does integrating along curve give?
NOTE: must rely on prior knowledge, when cannot derive information from image data

8. Level Set Segmentation (uses level set function? better than 7?)
  implicit as oppose to explicit boundary in 7.
  - in general define energy function that indicates if matching boundary
  - then iterative optimisation process to get it have closer fit 

## Evaluating Segmentation Methods
Truth pixels. Segmented pixels.
Four subsets:
  * true pixels fg
  * true pixels bg
  * false positives
  * false negatives
- Sensitivity (true-positive) how much fg/object is correctly segmented
- Specifity ... (false-positive) how much bg is correctly segmented
Reciever Operator Characteristics (ROC), plots Sensitivity/(1 - Specifity)
Better methods have higher area under curve (AUC)
- Precision (fraction of segmented object that is correctly segmented)
- Recall (fraction of true object correctly segmented, i.e. same as sensitivity)

## Improve Segmentation
1. reduce noise with pre-processing
2. post-processing with mathematical morphology (nonlinear, unlike earlier methods like Guassian, Laplacian etc. so repeated invocations don't cancel each other out):
  * binary images (i.e. black and white)
   
  represent fg pixels as a set of coordinates
  set operations: translation, reflection, complement, union, intersection, difference, cardinality

  - Binary Dilation
  structuring element is 3x3 like a linear kernel that is typically all fg
  for each pixel, if structuring element overlaps at this point, then include pixel
  as structuring element is symettrical, reflection not matter
    * cheaper computationally to do 3x1 dilatation and then 1x3 dilatation
  - Binary Erosion:
  for each pixel, if structuring element completely overlaps/subset at this point, then include pixel
  - Binary Opening (remove small elements, i.e. smaller than structuring element outside of image):
    * erosion and then dilation
  - Binary Closing (add small elements, i.e. smaller than structuring element inside of image):
    * dilation and then erosion
  - Edge Detection (produce inner and outer edges)
  difference between dilated and erosion
  - Object Selection
    with seed pixels in same area as object, iteratively build up with dilation
    (can do subsequent removing)
 
  Ultimate erosion computes distance transform (labelling with iterative erosion) and then find local maxima to get centerline
  NOTE: dilation reconstruction has seed pixels

  * gray-scale images
    - umbra is 3D binary image of grayscale (height, i.e. number of 1s is grayscale value, e.g. 255 equates to 255 1s)
    - dilation would be performed on umbra and then inverse umbra obtained
    dilation in grayscale will remove bits?
