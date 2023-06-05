<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Introduction
Computer science aspect of computer vision is developing theories and methods to extract visual information, e.g. write papers
Computer engineering implements these algorithms and software tools

Computer vision good for consistent, well defined data.
AI -> machine learning -> neural networks -> deep learning
For more generalised problems solved with AI, computer vision can still be used to refine the noise output from neural networks 

Human eye is susceptible to optical illusions.
More readily seen in say 'abnormal'/microscopic analysis, e.g. brain tumour cell analysis

Computer vision used in collision detection, autonomous monitoring (e.g. rover on Mars), OCR, object detection, medical imaging (image guided surgery)
It's a multiscaled operation: pixels -> regions -> objects -> multiple images
Low-level image processing, i.e. image in -> image out (enhance/suppress certain characteristics)
High-level image analysis, i.e. image in -> knowledge out (also involves using prior knowledge to acheive a better interpretation)
NOTE: (image analysis is features out. computer vision is interpretation out)

## Image Formation
An image is a 'interaction' of light reflecting off an object
So source of light affects the result

Light reflects off a single point on a object in multiple directions
So, a simple photosensitive plane will capture same point on different areas, creating a blurry image. 
A pinhole/aperture can be used to get a unique reflected light wave for each point.
Distance of aperture to image plane is focal length
A larger focal length will result magnification. 
As a result, distance, angles and areas are not preserved when projected onto the image sensor (perspective geometry)
Lens contains an aperture and helps to more intelligently block out light

Camera lens models RGB cones in our retina
RGB is limiting in expressing subtle colour changes
So, other colour scales:
  * HSV
    Hue is colour
    Saturation how much deviation from white
    Value is brightness
  * Y(brightness)Cb(deviation of blue)Cr(deviation from red) (good for compression)
  * LAB
    Lightness
    b (deviation of yellow to blue)
    a (deviation of red to green)
    This is most effective

Digitisation of continuous/analog image from film breaks image into grid and converts photon amount to a number, i.e.
digital image just a matrix of numbers (we have discretised it. )
sampling interval (how discretise image)
have digitisation in x and y.
also have digitisation in intensity (gray level quantisation). human eye generally distinguish only 100 levels of intensity
however, 256 as convenient mapping to byte

experiment with minimum number of pixels required to perform particular task well, e.g. 64x64 for human face recognition

input light distribution is what lens can capture. so, lens can only capture certain amount

## Image Processing (indicate what pixels are important)
1. spatial domain (image space):
  * point operations (individual intensity pixel transformations):
    - contrast stretching (all pixels lower than value go to 0, in between get scaled linearly, higher go to 255)
       + intensity thresholding is getting binary image, i.e. black and white (very useful for say object count. simplest form of image segmentation)
       IMPORTANT: good for identifying main object
       only good if background and foreground pixels don't overlap
       Various methods for automatic intensity threshold
       Otsu threshold (try all possible threshold)
       Isodata method (threshold is midway between two class means)
       Triangle thresholding (uses histogram; best for when no two distinct areas)
    - Multilevel thresholding if multiple areas of interest 
    - intensity inversion (flipping intensities)
    - log transformation (maps lower values to a wider range; look at curve)
    - power transformation (inverse of log transformation) (this is what is used for a gamma correction, i.e. too bright light source?)
    - piecewise linear transformation
    - gray-level slicing
    - bit-plane slicing (with bits, the more MSB, the more meaningful the value is)
    - arithmetic operations 
       (subtraction to determine what has changed between two images)
       (logical and with a white rectangle mask)
    - averaging (to reduce noise; better results with a higher value of N, i.e. averaging over same image multiple times)

    histogram counts how many pixels have particular intensities
    could show image is of low/high contrast
    normalising histogram is in effect generating a probability function

    (for images with complex histograms)
    histogram equalisation (equal distribution). contrast enhancement (make better use of ranges of colours)
    increases contrast between histogram peaks and reduce and troughs
    (contrast stretching for multiple ranges)

    turning histogram into a uniform distribution (TODO)

    a colour images has three histograms

    histogram matching (make one image look more like another?)

    histogram specification ()

  * neighbourhood operations (groups of pixels)
2. transform domain (fourier/frequency space)


IMPORTANT: appendix A szeliski numerical
