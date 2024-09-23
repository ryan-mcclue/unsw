<!-- SPDX-License-Identifier: zlib-acknowledgement -->

**The Challenge of Value Alignment: From Fairer
Algorithms to AI Safety**
## Value Alignment
Technology is never value-neutral, often embodying values of creators, e.g. Robert Moses bridges designed to divide white and black neighbours with underpasses etc. 
(This is exemplified by Langdon Winner's concept of artifacts having politics, referencing examples like Robert Moses's bridges in New York City (Winner 1980))

AI's ability to learn makes their actions less predictable; making value alignment more important.
Algorithms underpinning AI learning, amplify the biases in training data; yeilding 'algorithmic bias'
(Angwin et al. 2016; Lum and Isaac 2016).

1. Top-down approach:
Explicit ethical principles into AI systems. Challenging in defining universally acceptable morals.
2. Bottom-up approach:
Learn values from feedback. Difficult to know if learned values from biases in data.

Difficult to evaluate AI behaviour, e.g reward hacking to maximise reward without intended goal
Superintelligent AI accelerates these concerns.
So, aim to have technology systems embody the diversity of social/human values as oppose to single user's preferences. 
To ensure AI serves humanity as a whole, interdisciplinary collaboration essential for more socially aware technology.

**Interactions Magazine: Value-Sensitive Design**
Technology is not value-neutral, bearing creator's values often embedded unconsciously.
Consider human values throughout design process:
1. User autonomy (even small design choices like automatically recording microphone impactful)  
  - Capability: systems should provide users tools to acheive goal
  - Complexity: accessible to users
  - Misrepresentation: accurately represent capabilities
  - Fluidity: adapt to changing user needs
2. Freedom from bias
  - Societal bias: e.g. education software targeting male/female
  - Technical bias: e.g. guis not for visually impaired
  - Emergent bias: e.g. changing societal norms

Should incorporate bias mitigation techniques throughout design process. 
Important that technology reflects human values to promote a better future.

**Bias on the Web**
These biases interact, making mitigation complex. Furthermore, AI is trained on these biases.
1. Activity Bias
Small percentage of users create content/reviews etc., giving illusion of 'wisdom of the crowd'
2. Data Bias
English language content dominance; education requirements to access information
Web spam and content duplication exacerbate this.
3. Interaction Bias
  - search ranking bias 
  - presentation bias, i.e. more 'clickable' content
  - social bias, i.e. high reviews despite personal disagreement

Address with:
  - Focus on diversity of search results
  - Transparent algorithms

**Impossibility of Fairness**
Fairness is defined differently by different worldviews.
Automated decision making is therefore difficult to acheive fairness.
1. What You See Is What You Get (WYSIWYG):
Focuses on individual fairness.
Data reflects reality.
e.g. equal scores on test, equal students (ignores student priveleged background) 
2. We're All Equal (WAE):
Focuses on group fairness.
Data has biases that try to correct.
Different demographics have same potential, however structural biases distort data.

Understand fairness through features (inputs):
1. Construct Feature Space: not directly measurable free from bias, e.g intelligence
2. Observed Feature Space: measurable with bias, e.g. test scores
And decisions (outputs):
1. Construct Decision Space: who truly deserves from from bias
2. Observed Decision Space: made by algorithm with bias

No single algorithm can be fair from these worldviews.
e.g. WAE representational algorithm would modify data, while WYSIWG would pre/post process data

To address, explicitly state worldview and build in diverse values.
