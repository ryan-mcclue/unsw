<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TODO: docker for react and flask webserver

TODO: development environment
      scaffold project directory
      how do unit tests feature in machine learning?
      how are training, application and model weights stored?

brick/
  frontend/
  backend/
  Docker.yml  
  ci?

TODO: 
mobile app
(later can say exceeded optimisation expectations and able to make more accessible and use expo)

TODO: establish clear users for design justifications
  - industry user (accuracy)
    food safety inspector 
    restaurant manager
  - normal user/consumer (speed)
    (in a food mall purchasing food; want to know how long)

TODO: training
train on images assuming room temperature
then put through arhenius equation with humidity and temperature
to predict how long will last if say refridgerated etc.
these equation use values (like fruit decay rate) are pre-calculated
based on particular fruit that the model is trained to recognise.

TODO: multiple fruits problem
for each image, segment each fruit present.
then pass each into cnn to classify
group these classifications based on pre-existing heuristics for each fruit
alternative is to train models with these parameters, however training time too much

TODO: marking up data
fruits-360 dataset

