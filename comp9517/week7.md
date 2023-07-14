<!-- SPDX-License-Identifier: zlib-acknowledgement -->
# Deep Learning

1. start with a linear classifier (machine learning)
often cannot separate classes with lines
2. non-linear neural networks
   2 layer neural network: (more specifically a multi-layered perceptron or fully-connected network?)
   1. f = Wx (linear part)
   2. f = W2max(0, W1x)
   (these sections are activation functions?, i.e. each layer has one?)
   (W is a matrix of weights/parameters)

CNN vs NN?
CNNs, recurrent neural networks, etc. are deep learning (really just deeper architectures with more data/layers)
CNNs will gradually transform image at each layer, e.g. first lines, than sections, etc. 

Trained models like? Or actually architectures, e.g. structures to deal with difficulties training a deep neural network?
AlexNet, ResNet, GoogleNet? 

model can overfit if not good training data

different types of layers, e.g. convolution (sliding sum and multiplication with kernel), relu?, pool?
convolution layer is a linear layer (no activation function)
convolution produces activation map of depth 1.
n-convolutions produce activation map of depth n.
by increasing stride of convolution (i.e. pixel steps for sliding window), resulting output is smaller
can use padding to allow for any stride length

pooling just resizes activation map, e.g. average of local areas, max of area etc.

ConvNet is sequence of convolution layers interspersed with activation functions
TODO: So, a CNN has convolutional layers?

difference between fully-connected layer and ...?

A tensor is a multidimensional matrix?

impractical to have each layer be fully connected for large data sets, i.e. in deep learning
so the concept of local connectivity; each neuron only connected to a local region, i.e. its receptive field


fully connected is normal neural network (all neurons connected to input volume)

by determining loss, update the parameters in the neural network, i.e. train the network
backpropagation is optimisation as only compute loss for one layer and then backpropagate it?
so, want to find weights that minimise loss

training without validation or evaluation
training objective is just to minimise loss value.
however because of limited data set, training data set may overfit

can augment data artificially, e.g. add noise, rotate, cropping etc.

regularisation adds penalty to loss function to reduce overfitting
 * L1, L2 (modify cost function)
 * dropout (randomly drop neurons)

batch normalisation stables training and thereby accelerates it

most DL frameworks have various optimisation methods, e.g. internal covariate shift, batch normalisation etc. 

Applications: captioning, detection, classification, generation, etc.

NOTE: can use MobileNet for say FPGAs (IMPORTANT: so type of model choose dependent on research on specific problem)
Various different network models combine layers in different ways
But in all cases, have to learn weights/parameters for task

Unsupervised learning would generate possible class labels.
This would then be fed into a supervised model?
This is self-supervised learning?

## DNN Design Concerns 
1. Semantic Segmentation:
   * although output has each pixel with class label.
     have class label for centre of pixel region
     the CNN will classify centre pixel of a predefined region/patch size of pixels
   * will have convolutional layers and non-linear activation functions.
     however will have no pooling layers interspersed, as require output to be same size as input
     but for efficiency, will have a downsampling/encoder at start then an upsampler/decoder at end
   * unpooling/upsampling, e.g. nearest neighbour does not have parameters to learn like in pooling
     strided convolution is downsampling, transpose convolution is upsampling
     so two options for upsampling and downsampling?
   - Other tasks relating to pixel-by-pixel classification (i.e. model similar to this), e.g. unblurring, reflection removing, etc.
     In other words, dense prediction tasks that output pixel-wise map
2. Object Detection:
   * sliding window. bbox regions are proposed based on say HOG features
   however, typically integrate a region proposal network into entire network. 
   - one-stage methods like YOLO (i.e. single pass through DNN)
3. Instance Segmentation:
   * more advanced form of object detection. Uses similar architecture, however includes a mask prediction

RNN (recurrent) -> used for action recognition, image captioning (so better for advanced tasks that have sequential data?)
Also have generative NN models?
Also have Transformer based networks
