<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# Feature Representation

## What and Why
e.g. lightness representation of image -> classifier based on lightness value, e.g. lightness > 4.5

NOTE: a lot of algorithms have variations

Features are compact representation of image:
* colour (invariant to scaling, rotation, translation etc.)
  - histogram
  - moments (like stat values?, e.g first-order is mean, second-order is variance?)
* pixel-gradient/texture?
* Haralick Features
  - shows spatial relationship between pixels (distinguishes rough/smooth surfaces)
* Local Binary Patterns (LBP) (for comparison, must be on same resolution) 
  - describe spatial (texture classification)
  - cell of pixels 
  - can be altered to be rotation invariant 
    bit-shifting to find smallest number (as same numbers would be present). this might reduce 256 as number of bits changed
* Scale Invariant Feature Transform (SIFT) (very important):
  - describes texture features around keypoints? (match keypoints in different images of same object)
  - used in image stitching (could be use in robot to determine camera angle, i.e spatial transformation), object point matching/correspondance
  keypoint is greatest changes between structures (not necessarily largest difference, e.g. obtained with filters)
  1. Extrema detection
  DoG (difference of Guassian) at different scales to detect maxima and minima in scale space of image
  Increasing scales equates to increasing sigma for Guassian
  Get rough estimate of keypoints
  2. Keypoint Localisation
  Improve keypoints and find them in sub pixel space
  3. Orientation Assignment 
  Estimate keypoint orientation using gradient vector
  Create additional keypoints for orientation histogram peak
  4. Keypoint Descriptor
  Describe keypoints based on histogram of orientation, creating 128D keypoints

- once have keypoints; make determinations:
- by comparing keypoints can determine possible transformation, e.g. scaled, rotated, etc. (which can be represented as matrices)
- perform least squares fitting based on transformation matrix? 
  RANSAC better than this:
  * apply model to random points
  * see how many outliers and inliers (outliers in kurtosis showing tailedness)
  * repeat until highest value 

IMPORTANT: SIFT features are local features (Also have LBP, SURF, BRIEF feature identifiers)
Turn this into global features with Bag-of-Words (Also have VLAD, Fisher-Vector feature encoders):
  - Create a histogram of features, i.e categories of descriptors
  - In a sense, we develop a vocabularly from SIFT features
  1. create clusters (k-means) for each feature
  2. assign a feature cluster histogram, i.e. BoW encoding
  From establishing a vocabularly and train a classifier

(keypoints get most important information in image disregarding background?)
(so HoG better for smaller areas?)
* Histogram of Orientated Gradients:
 describes distributions of gradient orientations in localised areas
1. get gradient magnitude and orientation at each pixel 
2. divide orientations into bins
3. concatenate and block normalise cell histograms

* Shape Features
  - compactness, circularity
  - chain ...

* brightness
* edges
* corners
* lines
From features can do say:
* object detection
* segmentation (label subimages)
* tracking

Require feature map as artifacts introduced from camera cannot rely on pixel values alone, e.g. illumination, viewpoint, etc.
(also for efficiency)

pre-processing -> feature representation -> pattern recognition

Have classical and machine learning methods

## Learning Based Feature Representations
* Supervised (specific task)
 - deep neural networks (end-to-end model?)
* Unsupervised (generalised)
needs loss function to provide supervision signal? (GAN loss?)

Sparse Coding (before deep learning):
 - learn a BoW?

Autoencoder:
 - neural network trained with the task of reconstructing images


## How
Feature extractors/descriptors (classical and representation)
