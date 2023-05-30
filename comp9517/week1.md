<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Computer science aspect of computer vision is developing theories and methods to extract visual information
(this also involves optimally using prior knowledge to acheive a better interpretation)
Computer engineering implements algorithms and software tools

Computer vision good for consistent, well defined data
Output of a neural network still has a lot of noise, i.e. error margins
So computer vision, still used to refine this output for more general tasks. 

Human eye is susceptible to optical illusions (more paramount for microscopic analysis, e.g. brain tumour cell analysis)

Collision detection, autonomous monitoring (e.g. rover on Mars), OCR, object detection, medical imaging (image guided surgery)

Computer vision is multiscaled: pixels ➞ regions ➞ objects ➞ multiple images

low-level cv, i.e. image processing, i.e. image in - image out (enhance/suppress certain characteristics)
high-level cv, i.e. image analysis, i.e. image in - knowledge out

image is 'interaction' of light reflecting off object (so source of light is important for result)

want to capture unique points of reflected light to not look blurry, i.e. each point will be reflected in many different directions
could have pinhole/aperture

camera lens models RGB cones in our retina

rgb inefficient

HSV
hue is colour
saturation how much deviate from white
value is brightness

Y(brightness)Cb(deviation of blue)Cr(deviation from red) (good for compression)

LAB
lightness
b (deviation of yellow to blue)
a (deviation of red to green)
(changes more to what the eye percieves)



TODO: appendix A szeliski numerical
