<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# Image Motion
Add time as dimension to image
Allows to analyse differences -> trajectory -> motion (more complex object detection on motion)

Can have still or moving camera

IMPORTANT: Because of this, computer vision is largely probalistic rather than deterministic
## Change Detection
IMPORTANT: Always assumptions in success of computer vision algorithms, e.g. lighting conditions remain the same, distance of object to camera similar
Moving across constant background:
  * small motion: image subtraction

## Motion Vector
Motion vectors (sparse motion field) representing displacement of objects
Compare the correspondance between pairs of points from images (use unique points with texture,variance,contrast)
To find point in other image, compute a patch that is similar (window matching reduces search space; will need to know expected motion)
Have various similarity measures, e.g. absolute-differences, cross-correlation, mutual-information (constructs a 2D histogram from 1 from each image; more robust for lighting variances)

## Dense Motion Estimation
Motion for each pixel 

Taylor Series is estimating/approximating function value with a delta added, e.g. f(x + delta) = f(x) + f'(x)·delta
Optical Flow equation f(x + delta, y + delta, t + delta)
Lucas-Kanade approach uses least-squares to solve optical flow
Optical flow gives velocity vector


## Tracking
IMPORTANT: Assume smooth movement, no objects overlapping
Motion for a sequence of images
Difficult due to spatial dimensions lost from 3D world to 2D image, e.g. noise, occlusions, etc.

Bayesian Inference (iterative prediction and correction):
  * Moving object has state; a random variable which contains anything of interest, e.g. position, shape, intensity etc. (Xs)
    Measurements performed at each time point (Ys)
    So will have P(X|Y), i.e. probability have state X given current measurements
    After this, will use new Y to correct predicted X
  * Must design: Dynamics Model P(X|X-1), Measurement Model P(Y|X)
  * can be implemented with kalmann filters (assume distributions are guassian, so can describe with mean and standard deviation) 
    so everything becomes matrix multiplications
  * also implemented with particle filtering if non-guassian distribution.
    propagate each sample using dynamics model and obtain new weight with measurement model

if probabilty, than expressed as a distribution?
conditional probabily P(X|Y), can be written as a joint probability (just probabilities multiplied/divided etc.?)

