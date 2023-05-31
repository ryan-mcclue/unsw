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

## Image Formation
An image is a 'interaction' of light reflecting off an object
So source of light affects the result

Light reflects off a single point on a object in multiple directions
So, a simple photosensitive plane will capture same point on different areas, creating a blurry image. 
A pinhole/aperture can be used to get a unique reflected light wave for each point.
Distance of aperture to image plane is focal length
A larger focal length will result magnification. 
As a result, distance, angles and areas are not preserved when projected onto the image sensor
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


IMPORTANT: appendix A szeliski numerical
