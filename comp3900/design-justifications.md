<!-- SPDX-License-Identifier: zlib-acknowledgement -->

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


