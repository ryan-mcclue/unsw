<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Neighbourhood Operations (groups of pixels):
Also called filtering techniques
Take group -> output single
The group size, a.k.a kernel, window etc. (convolution uses kernel terminology)
The kernel will have values that we will use on input region  
 
Convolution means to combine, i.e. multiply and add neighbours
Therefore, convolution more involved than basic multiplication
properties satisfied by convolution:
  * linearity (allows for breaking down problems into smaller steps, i.e. operation of linear combination, same as each individual)
  * shift invariance (if shift in space, does not discriminate between spatial positions)
  * commutativity, associativity, etc.

Border problem (border pixels don't have available pixels) fixes:
* zero padding (add a border of 0)
* clamping (duplicating final pixel)
* wrapping (implicitly used when using Fourier?, as creating a periodic image)
* mirroring (periodic image, but with half the rate of wrapping)

Filters:
When asked what filter to use, ask yourself what you want to keep, and lose
- Smoothing Filter (remove noise, but also detail): 
  * mean pixel value (blurring), i.e. uniform filter (kernel is uniform, i.e. all 1s)
  TODO: weighted average, i.e. divide by all values added to normalise? as in daves garage?
  smoothing is removing higher intensities, i.e reducing slope
  * guassian filter: pixels closer to the centre have greater weight
  use when small objects retained
  slowy varying in spatial: frequency has very narrow range
  narrow in spatial, wide with fourier domain
  repeating low-pass filter convolution converges to Guassian
  guassian infinitely smooth, i.e. can derive at any degree
  (the standard deviation of the bell-curve used to create the Guassian kernel is important) 
  (in general, giving more weight to the pixels closer to current pixel)
  * median filter: median pixel value in neighbourhood (eliminates high intensity spikes)
  use when small objects must be removed

* unsharp mask: want to enhance rapid changes

* pooling: filtering and downsampling, i.e. reduce image size to reduce operation time

image derivates obtained by differences, e.g. forward/backward/central difference
so f(x + 1) - f(x) first order derivative in x
i.e. derivatives used to construct filter? 

TODO: how are derivative kernels obtained?

Laplace is integral transform that converts real to complex 
Laplacian is 2nd order derivative. uses symmetric kernel
Therefore, more sensitive to noise than first-order
Sobel/Prewitt measure the slope while the Laplacian measures the change of the slope. 

derivative of image obtained by convolving with derivatie kernel obtained from guassian function

derviate in one direction, keep same profile in another
so differentiation in one dimension and smoothing in another dimension
taking derivative is taking more frequencies, i.e. more noise to be added 
(so to temper this, only derive in one direction), e.g. derive in x, smooth in y
differentiation suppresses low frequencies, blows up high frequencies

TODO: convolution is in effect a weighted average?


have uniform, prewitt, sobel and guass kernels
prewitt and sobel are first-order derivative kernels
(TODO: are these all greyscale operators?)
take for example sobel:
* will have a kernel for x direction, i.e. how strong is edge is vertically
* will have a kernel for y direction, i.e. how strong is edge is horizontally
* now using pythagoras, find magnitude of edge, i.e. product of sobel edge detector
* atan(gx/gy) gives edge orientation
IMPORTANT: as small kernel size, will pick up false edges, i.e. more noise
so, usually apply guassian filter first to remove high frequency stuff
after applying convolution, remap into 0-255 (as could be negatives)


using separable filter kernels yeilds less FLOPS

combining filters to say enhance edges?

gradient is vector of first order derivatives
points in direction of steepest intensity increase
gradient magnitude (useful to compute edges; laplacean also used for edge detection)

laplacean also used for sharpening  

https://edstem.org/au/courses/11999/discussion/1425954

https://www.reddit.com/r/learnmath/comments/rcgj3r/is_there_a_simple_function_that_equals_1_when/
