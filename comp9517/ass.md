<!-- SPDX-License-Identifier: zlib-acknowledgement -->
RECORDING: and when they start presenting, they must mention their name.

## Literature Review
Review relevant techniques in literature, along with any necessary
background to understand the methods you selected.

TODO(Ryan): Just reference lecture slides for others?

A border following algorithm plays an important role in detecting image contours. It starts by finding a boundary pixel and moving this to a neighbouring boundary pixel for as long as possible. The particular connectivity scheme in use determines what neighbouring pixels to consider, e.g. vertical, horizontal, diagonal etc. The result is an effective trace/outline of edges in an image. However, this lacks certain topological information. Specifically, all edges are not uniquely identified, their specific coordinates are absent and the relationship between edges are not known. Contours can be defined as edges with this information added, i.e. an augmentation of the border following algorithm. By adding this data, the contours detected can be considered hierarchical structures representing continuous curves as a series of (x, y) points. This allows for further shape analysis such as determining contour areas, heights, widths, etc. 

This additional information present in contours was utilised in computing possible bounding boxes. 

https://www.sciencedirect.com/science/article/abs/pii/0734189X85900167 

Genetic Algorithms (Ryan) 

To perform object detection there are a large number of non-constant factors to be considered that make it a complex problem to solve using traditional computer vision techniques. Such factors include rotation, translation, scale, lighting, occlusion, colour etc. For an object in question, a series of features extracted from an image can constitute a detection. Therefore, if these features are found in an image, the object can be considered detected. The large number of possible feature permutations means this can be considered an exhaustive search problem. To reduce computational effort in finding these features, a genetic algorithm can be used. This class of algorithms are intended to optimise problems involving large search spaces. By modelling the process of natural selection, solutions are iteratively refined via mutation, crossover and fitness evaluation. 

The foundations of this method inspired the use of a genetic algorithm to optimise the search of hyperparameters for contour detection that led to bounding boxes of greater IOU. 


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

Everyone - have slides and notes on your own model/methods

Ryan McClue - can you create a visual demonstration of how your model works
(with focus on the unique aspects like the genetic algorithms), 

and maybe an animation of the raw image being segmented into bounding boxes?
(draw contours? then their boxes?)
