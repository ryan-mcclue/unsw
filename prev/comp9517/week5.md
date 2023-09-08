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
  However, conditional probabilities might have conditional risk, i.e. cost if wrong. 
  This will be loss function, e.g. pSalmon_wrong = 0.1
  So, optimal Bayes is to minimise conditional risk
  TODO: distinction between decision and classification?
  4. Decision Tree
  Represented as tree with each node being an 'if statement'/feature. leaf nodes are labels
  Nominal data is also catageroical
  To determine what feature to split on use information theory (entropy and information gain?)
  Entropy considered average uncertainty of data
  Calculate entropy with formula, inputting prior probabilities of type, e.g fish type
  Base entropy is just how often type appears in training
  Information gain based on entropy. 
  Use feature with highest information gain to split on in the decision tree (based on formula)
  5. Ensemble Learning
  Combines multiple models.
  Random forests construct an ensemble of decision trees. Uses Breiman's algorithm, which uses randomness to construct trees
  Works best if trees in forest are uncorrelated
  Overcomes decision tree overfitting issues (overfitting is major problem in Machine Learning)

  * Regression
  Want a line that has outputs match features?
  Is different approach to normal classification? (i.e. different to SVM?)
  Has its own unique error values, e.g. root mean square error?

TODO: class is areas belonging to same label?

Separate models?
## Binary Classifiers
Separability, i.e. linear separable would be able to draw straight line between object classes
Linear classifier uses linear separating function, e.g. w1x1 + w2x2 + ... b. 
If f(x) > 0 then 1, f(x) < 0 then -1 (so linear classifier is for a binary problem? e.g. cat or dog?)
Training data learns weights and offset (x's are features)
Support Vector Machines (SVMs) is used to maximise distance between classifier line and closest sample (i.e. optimise weight and offset values)
(in general hyperplane to closest samples for dimensions greater than binary)
HOG, SIFT, BoW features given to SVM
Hard Margin SVMs if linearly separable. 
Soft Margin SVM introduces 'slack' variables to allow for misclassification, i.e. when one object might be grouped closely to other object 
For completely non-linear boundaries, convert data to hyperplane

## Multiclass Classifiers
Can do with binary classifiers, i.e. for each class define a classifier for that single class and all other classes

## Evaluate Classification Error
Error rate, reject class (generic class for objects not belonging), etc.

false positive/false alarm/type 1 error
false negative/false dismissal/type 2 error (typically worse)

Reciever Operating Curve (ROC) relates false positive to the true positive (if area under curve is high, classifier is good)

Confusion Matrix is 2D where (i, j) is how many times i was put in class j. So high diagonal good

F1 score is harmonic mean


Cross Validation used to evaluate all models, e.g. SVM and regression




