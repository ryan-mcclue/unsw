<!-- SPDX-License-Identifier: zlib-acknowledgement -->

both chemical engineers in food science
rishi food processing firm (how would use technology)

plantuml for diagram?

Group images:
  - if giving an average value, then output boxes below fine
  - however seems like more useful to user if bounding boxes on each individual fruit
    on that bounding box provide best-before and freshness

1. Are we attributing rotten/best-before for each individual fruit in the image?
2. Are we outputting freshness and best-before or only one?
I'm confused when it says average it out.
For example, say 1 banana is rotten out of 5 bananas.
Do you output fresh, as most are not rotten?
What is the best-before in this case?

Model training:
  Model 1 (CNN fresh classifier)
    fresh, not fresh photos?
    would this also output type of fruit?
    how would temperature and humidity info come into this?
  Model 2 (random forest regressor best before)
    same data set except different feature extraction? e.g. color and shape?

TODO: how to incorporate location data to neural network?

Include a list of design justifications for your planned solution.
• This should include:
(i)
Decomposed Subproblems:
  - Dataset Collation problem
      tagging with location data?
      data augmentation techniques?
  - UI problem
      realtime:
        - Develop progressive loading techniques for partial results display 
        - Implement parallel processing for different analysis tasks
      location detection:
        - Implement GPS-based location detection (with user permission)
        - Allow manual input of location
        - Use IP-based geolocation as a fallback
      acessibility
      user text input

  - Video handling problem
      revolving video
      temporal segmentation
  - Group fruit problem
  - Freshness problem
     model selection
     feature extraction? 
     layer selection?
  - Best Before problem

  - Basic subproblem
    how to solve ...
  - Complex subproblem
    how to solve ...
    alternative solution 1 ..
    why chose ours ...
(iv)
Extended functionality beyond existing systems:
  existing systems do ...
   
   native application affect accessibility (could compile with wasm)
   online requirements for location data (prestored database of location values)

A discussion how your solution provides novel functionality beyond
existing systems wherever relevant in your design justifications.
Effective design justifications will incorporate research from the background
section, identify how decisions will affect users and identify possible limitations
in your design and how you will mitigate these.


