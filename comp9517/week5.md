<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Pattern Recognition
E.g. objects, text, events/actions

Based on machine learning paradigms:
Weakly supervised uses noisy labels

TODO: conference mentioning for assignment inspiration?

Supervised Learning:
  * Classification
  Processing of assigning labels/categories. 
  Will design a classification system which has steps, e.g. pre-processing, feature extraction, learning system etc.
  Training samples are ones with labels
  Models are description of classes
  Types of features, i.e. feature vector, particular to task, e.g. colour, lightness etc. (ideally want invariant to say rotation, occlusion etc.)
  - Generative Model:
  unsupervised. class represented by probalistic model
  - Discriminative Model:
  supervised. more explicit model
  
  1. Nearest Class Mean Classifier
  Centroid of class, i.e. mean
  Compute distance between centroid of classes
  NOTE: class could be located in multiple areas, e.g. have multiple modes
  2. K-Nearest Neighbours Classifier
  Decides class label based on K nearest samples,
  Distances between the test sample and all training samples are computed
  The neighbours are selected from a set of training samples for which the class is known
  The sample will be assigned to the class which has the majority of members in the neighbourhood
  Hamming distance for discrete variables (otherwise Euclidean)
  3. Bayesian Decision Theory 
  Probalistic decisions. 
  Consider how our classes were generated, to generate probabilities.
  Incorporates prior probability, e.g. pSalmon = 0.8, pBass = 0.2
  Also conditional probability, e.g. pSalmon_len > 50cm = 0.4
  Posterior probability is prior * conditional. The conditional we must input
  Assign class with highest posterior probability (which is just what Bayes Decision rule is)

  * Regression

TODO: class is areas belonging to same label?

