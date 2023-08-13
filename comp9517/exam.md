<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Each paragraph should include a topic sentence stating its main point. It is advisable to put the
topic sentence at the beginning of the paragraph so that it is immediately clear what will be
discussed in that paragraph. The remainder of the paragraph should then elaborate on this using
facts, arguments, analyses, examples, or any other useful information, and conclude by
connecting back to the main point.


## AI
TODO: neural network usage as in DODO
* AI for more general purpose; traditional to refine the noise output (binary morphology) from neural networks (refine input in case of segmentation)
* Unsupervised learning would generate possible class labels.
This would then be fed into a supervised model?
This is self-supervised learning?
* If using say a MobileNet architecture, more applicible scenarios
## Preprocessing
* Histogram equalisation then multilevel thresholding
* Genetic algorithm for hyperparameters
* Ensembling of local feature types SIFT, SURF etc. for BoW
  Ensembling segmentation methods
  Ensembling classifiers
  (stacking based ensemble, i.e. combine classifiers with logistic regression. then ensemble results with probability voting)
* Break into stages, e.g. first detect if something there, then define (to allow for further ensembling compensating for weaknesses)
* DFT operations to limit FLOPS for convolution in higher dimension kernels
* Look at different evaluation metrics?
IMPORTANT: Because of this, computer vision is largely probalistic rather than deterministic
IMPORTANT: Always assumptions in success of computer vision algorithms, e.g. lighting conditions remain the same, distance of object to camera similar
NOTE: timelapse tracking will require terabytes of data for long periods of time
## Results
high recall (ability to find positive), low precision (many false positives)
most networks convolutional, i.e. have convolution layers
residual neural network (resnet) used for training deep networks by having 'skip/shortcut connections', i.e. not updating along all nodes
batch normalisation layers for deeper neural networks
ReLu (rectified linear unit) is an activation function


1. Introduction: 
Summarise the overall problem addressed in the paper.
Discuss which aspects of the problem the authors aim to solve and why these are important. 
Also discuss who will benefit if the problem can indeed be solved and how this may change the current practice in the field.

2. Methods: 
Summarise the methods used in the paper. 
Describe the reasons why these methods were chosen and discuss what the strengths and weaknesses of the methods are. 
Also, based on what you have learned in the course, discuss whether you think the authors made the right choices,
and suggest other methods that may have worked better.

3. Results: 
Summarise the experimental results presented in the paper. 
Discuss the used evaluation strategy and the implications of the main findings. 
Also, comment on whether and why you think these findings will convince potential users to adopt the proposed method, and suggest other
experiments that could have been conducted to make a more convincing case.

4. Conclusions: 
Discuss what you believe are the main strengths and weaknesses of the presented work as a whole (not just the proposed methods discussed above). 
Also, discuss the remaining technical issues that still need to be addressed before the problem stated in the introduction can be
considered solved, and suggest recommendations for future research.

References: List the literature references you have used in writing your commentary. This section is
not mandatory and will not attract points, but if you have used other works to better understand the
problem and come up with possible alternative solutions, and especially if you rely on them in
making any claims in your commentary, you should list those works and cite them in the text.>
