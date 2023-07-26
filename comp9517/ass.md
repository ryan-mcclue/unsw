<!-- SPDX-License-Identifier: zlib-acknowledgement -->
use IEEE overleaf template for report
make title like "Genetic algorithm with neural network ensemble"
watch in wk10 consultation then overflow into lecture as cannot watch all videos

https://docs.google.com/document/d/116BPTJ-hUhcxuee4d-eX56j7eNPp76EqDtLiif75ZTs/edit?invite=CIrp__AB

## Literature Review
Review relevant techniques in literature, along with any necessary
background to understand the methods you selected.

TODO(Ryan): Just reference lecture slides for others?

Centeno, Tania & Lopes, Heitor & Felisberto, Marcelo & Arruda, Lúcia. (2005). Object Detection for Computer Vision Using a Robust Genetic Algorithm. 284-293. 10.1007/978-3-540-32003-6_29. 
Equates object detection as an exhaustive search problem. 
Suggests a genetic algorithm to spend less computational effort to find properties describing object

## Method
Motivate and explain the selection of the methods you implemented, using
relevant references and theories where necessary.

A series of possible bounding boxes for the penguin/turtle in an image were calculated from extracted contours and keypoints. 
The applicability of this method was determined based on prior knowledge of the image set.
Specifically, knowledge that each image contained a single animal and that animal was the primary point of gradient complexity, i.e. dominant figure in the image.
Therefore, contours of relatively large area should correlate to the animal's outline and the mean/standard-deviation of keypoints should relate to the animal's location.

The steps of the algorithm were:
  1. **Noise removal**
  Image converted to grayscale and a bilateral filter applied.
  This type of filter was used as it preserves the edges of the image to greater extent compared to other filters, e.g. Gaussian.
  2. **Thresholding**
  An adaptive threshold was used over binary thresholding as images did not present histograms with well defined binary peaks. 
  Binary dilation was used to fill in the gaps between foreground segments.
  3. **Edge Detection and Contour Finding**
  Canny edge detection produces output that reduces noise for subsequent contour finding
  5. **Contour Bounding Boxes**
  Bounding boxes corresponding to the contours of largest area, width and height
  6. **Keypoint Detection**
  SIFT keypoints used due to their distinctiveness and repeatibility, i.e. consistently detect across images of different lighting/viewpoints
  7. **Keypoint Bounding Boxes**
  A bounding box based on the mean and standard deviation of the keypoints
  8. **Bounding Box Augmentation**
  A bounding box that was the union of the keypoint and largest area contour bounding boxes.
  Additionally, this unioned bounding box duplicated, except its centre is programmatically determined from thresholding. 

The hyperparameters feeding into each step of this algorithm affect the accuracy of the output bounding boxes.
To evaluate the accuracy of all the large number of hyperparameter permutations would be computationally expensive.
Therefore, to reduce the search space, a genetic algorithm was used that optimised the IOU of the bounding box calculated from largest contour area.
This box was chosen as it had the highest average accuracy across the training images.
The steps of this algorithm were:
  1. **Initialise Population**
  An individual represents a class of attributes corresponding to hyperparameters
  A population is a collection of individuals for the 10 images the original detection performed worst on.
  2. **Evolve**
    For each generation:
    - Compute fitness as IOU 
    - Parents selected from population based on highest fitness
    - From parents, create new individual who has half attributes of each parent
    - New individual has attributes randomly mutated
    - New individual is added to next generation
  3. **Result**
  The attributes of the fittest individual from the evolution simulation were used as final hyperparameters
  

## Experimental Results
Explain the experimental setup you used to evaluate the
performance of the developed methods and the results you obtained.

To verify the validity of each step in the bounding box algorithm, visual debugging was used.
Specifically, the output of each step were cached and later displayed sequentially.
The resulting bounding boxes were drawn atop the original image with text labels indicating their type.
This allowed for modification at each step and to see if such changes produced better results.
![Visual Debugging](visual-debugging.png)

Once the algorithm steps were defined, the most accurate bounding box was determined.
This was acheived by computing the minimum, maximum and average IOU for all bounding boxes accross all the training images.
The bounding box corresponding to the largest area contour unioned with keypoint was found to have the highest average, i.e. best performer.
Therefore, this box was optimised by the genetic algorithm.

## Discussion
Provide a discussion of the results and method performance, in particular
reasons for any failures of the method (if applicable).

For majority of images, the augmented bounding box most accurate:
![Augmented Best Bounding Box 1](aug1.png)
![Augmented Best Bounding Box 2](aug2.png)
![Augmented Best Bounding Box 3](aug3.png)
![Augmented Best Bounding Box 4](aug4.png)

For some images where the background features construct contours of largest area, the width and height bounding boxes are the most accurate.
![Height Best Bounding Box](height.png)
![Width Best Bounding Box](width.png)

For some images with strong shadows, the keypoint bounding box is the most accurate as contours mistake shadow for animal.
![Keypoint Best Bounding Box](keypoint.png)

For some images where the colour of the animal closely matches the background, the centered bounding box is most accurate as keypoints can focus in on colours different to background 
![Centered Best Bounding Box](centered.png)

For some images with complex histograms and gradient distributions, no accurate bounding box is found as no feature correlation to animal location.
![No Accurate Bounding Box](no-accurate.png)

Genetic Comparison:
![Genetic Comparison Bounding Box 1](comparison1.png)
![Genetic Comparison Bounding Box 2](comparison2.png)
![Genetic Comparison Bounding Box 3](comparison3.png)
IMPORTANT(Ryan): not sure if actually better with genetic algorithm as run on small population size for speed
it does work better for some images, but not overall
included for creativity...

TODO(Bill): Mention as no 'perfect' bounding box, tying in with classification better as can select what is better
e.g. Clearly if prior knowledge of contours not met, cannot definitively say what is best bounding box, etc.

TODO(Bill): Final numerical results here, i.e. based on the bbox from the neural network
(from spec)
"For each validation image, calculate the distance between the centre
location of the predicted bounding box and the centre location of the corresponding true
bounding box (available from the annotation file), and report the mean and standard deviation
of the distances over all validation images. Also calculate the intersection over union (IoU) of
the predicted bounding box and its corresponding true bounding box for each validation image
and report the mean and standard deviation."


## References
