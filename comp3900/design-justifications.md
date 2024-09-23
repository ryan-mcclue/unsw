<!-- SPDX-License-Identifier: zlib-acknowledgement -->
prior to uploading, mention clauses for accuracy, 
e.g. range +- days available;
perhaps popup if video does not align with expected conditions;

two outputs:
 1. range for refridgerated
 2. range for room temperature

get output for average person can see how long can use food for

output won't taste better after this many days?

so just shape and colour

wong:
  - food processing (plant-based food)
  plenty of existing techniques for food classification
  we want automatic implementation of these

rishi:
  - for daily consumer; 
    people are unaware 

food mall purchasing food; know how long

  14days max. apple-5days

Users:
  - food safety inspector 
  - restaurant manager
  - normal user
## Problems
**Scope Creep**
There exists many permutations of fruit 

varied fruit types; only look at subset of species; qualify this in app 

**Dataset Collation**
  Problem Summary:
Obtaining diverse datasets of fruits that represent a wide variety of types, 
stages of freshness, and environmental conditions (like temperature/humidity etc.)

use baseline number of fruits to ensure working

IMPORTANT: how to tag data with numerical values, e.g. 3days before etc. 

  Solution and Justification: 
Use public datasets like Kaggle as a base.
Where needed, supplement these with custom-collected data that include a broader range of fruits, vegetables, and freshness levels.
e.g. have to append best-before to fruit names

      tagging with location data?
      source of data?
      data augmentation techniques?

  We will collect diverse datasets containing images and videos of various fruits and vegetables. 
Public datasets like Kaggle provide a good starting point. 
Preprocessing will involve resizing images, normalizing pixel values, and augmenting data (rotation, flipping, etc.).
Justification: Preprocessing ensures that the data fed into the model is uniform, reduces overfitting, and increases the model’s robustness to variation in input data.

**Training**
Training complex models like CNNs requires significant computational resources, 
especially GPUs, which may not be available locally.

Training Convolutional Neural Networks (CNNs) 
can be time-intensive, especially when dealing with large datasets and deep architectures.

Transfer Learning:
Use pre-trained models like YOLO or AlexNet and fine-tune only the final layers, 
which reduces training time and resource requirements.
Model Optimization: Use lightweight architectures such as MobileNet or SqueezeNet, 
designed for efficiency on CPUs without sacrificing too much accuracy.

Justification: These methods reduce the need for local high-performance computing. Transfer learning and model optimization specifically minimize computational load, 
**UI**
Ensuring the user interface provides a seamless experience, 
handling real-time data, location information, and accessibility considerations.

Real-time Processing: Implement progressive loading techniques for displaying partial results as they are generated. 
Parallel processing will be used to handle different tasks concurrently, such as image analysis and location detection.
Location Detection: Use GPS for accurate location tagging (with user consent), allow manual input of location, and use IP-based geolocation as a fallback for location-based metadata.
Accessibility: Ensure the interface is accessible by compiling to WebAssembly (WASM) for native-like performance on the web. For users with poor connectivity or no GPS access, maintain a prestored database of locations for easy lookup.
Justification: Real-time feedback enhances user experience by providing immediate insights, while progressive loading and parallel processing ensure that users don't experience significant delays. Incorporating multiple location detection methods ensures flexibility, and WebAssembly improves accessibility for broader use.

      realtime:
        - Develop progressive loading techniques for partial results display 
        - Implement parallel processing for different analysis tasks
      location detection:
        - Implement GPS-based location detection (with user permission)
        - Allow manual input of location
        - Use IP-based geolocation as a fallback
      acessibility
      user text input

   native application affect accessibility (could compile with wasm)
   online requirements for location data (prestored database of location values)

**Handling Video Input (complex)**
Handling video input for freshness analysis presents challenges like temporal segmentation and continuous assessment over time.

Revolving Video & Temporal Segmentation: Implement temporal segmentation techniques to analyze key frames at intervals, extracting relevant features for freshness detection and degradation over time.
Justification: Video input allows for more dynamic and comprehensive analysis compared to static images. By analyzing videos, the model can adapt to real-time freshness and degradation scenarios, improving accuracy in retail or agricultural environments.

Advantages:
    Computational Simplicity: Using 2D CNNs on key frames is computationally less expensive than training a 3D CNN. Each frame is treated as a static image, so the model doesn’t need to learn temporal relationships between frames, reducing the complexity and computational burden.
    Less Data and Training Time: Since the model only processes selected frames, you can avoid dealing with the entire video, which saves both memory and computation. This leads to faster inference and shorter training time.
    Easier Implementation: Implementing temporal segmentation is relatively straightforward, especially if you're leveraging existing 2D CNN architectures. Many models are well-optimized for 2D images, with pre-trained models (e.g., ResNet, MobileNet) readily available.
    Flexibility: It allows for different segmentation strategies (e.g., equal time intervals, changes in brightness) to capture key moments relevant to the freshness assessment without overloading the model with unnecessary data.

Disadvantages:
    Loss of Temporal Information: By treating each frame independently, temporal segmentation loses the relationship between frames. This can be critical for analyzing progressive changes in freshness, such as subtle visual degradation that occurs over time.
    Reduced Contextual Understanding: The model will analyze individual frames without understanding the temporal progression. For example, it may miss gradual ripening or changes in appearance that happen over longer periods if key frames don’t capture these transitions effectively.


      revolving video
      temporal segmentation
Video input provides more information than static images, 
allowing for continuous analysis of fruit freshness and degradation over time, 
making the model more adaptable to real-world scenarios like retail environments.

**Group fruit problem (complex)**
Classifying and grading multiple fruits grouped together (e.g., in a basket or on a shelf) instead of focusing on single fruits.

TODO: is this just training on images of groups instead of single?

Training on Group Images: Collect and label images with groups of fruits, and modify the model to detect and classify individual fruits within a group, similar to object detection tasks.
Justification: Group fruit classification is essential for real-world applications like supermarkets or farms, where fruits are rarely analyzed individually. This makes the model more practical for use in large-scale environments.

**Predicting Freshness (complex)**
The need to classify fruit freshness, which is a complex task requiring advanced feature extraction and selection of an appropriate CNN architecture.

CNN Model: Use a Convolutional Neural Network (CNN) architecture with layers fine-tuned for multiple fruits and vegetables. Feature extraction can be performed using convolutional layers to capture textural, color, and shape information.
Justification: CNNs are well-suited for image classification, as shown in previous research (e.g., Bhargava and Bansal, 2020). By extending this approach to a variety of produce and adding video input, the model will be more robust and capable of handling more complex classification tasks.

     use CNN
     model selection
     feature extraction? 
     layer selection?
Solution: We will use a Convolutional Neural Network (CNN) architecture, fine-tuned for multiple fruit and vegetable types. CNNs are known for high performance in image classification tasks and are ideal for distinguishing visual characteristics of produce.
Justification: CNNs have proven effective in existing research (e.g., Bhargava and Bansal, 2020; Amin et al., 2023) with high accuracy in image classification. We will address the limitation of prior works by extending the classification task to a greater variety of fruits and vegetables and using video input.

**Predicting Shelf Life (complex)**
Predicting the shelf-life of fruits and vegetables using factors such as environmental conditions (e.g., temperature, humidity) and visual data.

Random Forest/XGBoost Model: Use Random Forest or XGBoost models to predict shelf-life, incorporating both visual data (e.g., hue) and environmental data (e.g., temperature, humidity) to make predictions.
Justification: Existing research (Reka et al., 2024) has shown the effectiveness of hue-based analysis for shelf-life prediction. By combining this with environmental factors, our model will improve prediction accuracy and provide more detailed insights into fruit and vegetable longevity.

  use random-forest/XGBoost
Solution: We will integrate environmental data (temperature, humidity) into a separate machine learning model, like a Random Forest, to predict shelf-life. This will be combined with hue-based analysis from the image data.
Justification: Research (Reka et al., 2024) has shown that using hue value in fruit images can be effective in shelf-life prediction. By introducing additional environmental factors, we expect to improve accuracy beyond existing systems.
