<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Games (board games, dice games, card games)

Uncertainty due to partial observability, noisy sensors, immense complexity of modelling real world
World model properties now have probabilities associated with them (probability theory)
Utility theory represents preferences, e.g. prefer outcome of this over that
Decision theory = u + p

P induces a probability distribution for any random variable X:
* boolean/propositional: cavity = true
* discrete: weather = snow, rain, sun
* continuous: temp = 21.6
∨ (OR), ∧ (AND; think intersection of Venn diagram), ¬ (NOT)
P(A∣B) = `P(A ∧ B)/P(B)` (conditional probability: probability of A given B has occured) 
Bayes rule rewrites this. Can do P(Cause|Effect) = `P(Effect|Cause)P(Cause)/P(Effect)`
For a medical diagnosis, have 2 random variables: cancer, test works
priors: P(positive|cancer) = 0.98, and P(negative|¬cancer) = 0.97

joint probability distribution is a table providing probabilities of all combinations of random variables (sum to 1)
P(A,B) is joint probability of events occuring simultaneously
Independent if have no affect on the other, e.g. P(A|B) = P(A)   

P (Catch | Toothache, Cavity) = P (Catch | Cavity)
We say that Catch is conditionally independent of Toothache given Cavity.

Identifying independent and conditionally independent variables, can reduce joint probability distribution table size

TODO: Use fringe models for Wumpus world?

Joint probability distribution specifies probability of every atomic event
➛ Queries can be answered by summing over atomic events
➛ For nontrivial domains, we must find a way to reduce the joint size
➛ Independence and conditional independence provide the tools 
