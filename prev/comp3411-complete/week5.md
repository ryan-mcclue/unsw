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

Wumpus world:
We know have safe breezes in 3 squares.
Joint probability: `P(pit11,pit12,...,breeze01,breeze02,breeze03)`
Conditional: `P(breeze|pits)P(pits)`
P(pit|known,observed) = proportional to all unknown (however don't care about all unknown)

Prior know pits in `16C3 = 16!/(3!*13!) = 560`

posterior: P(cancer|positive) estimate after data observed

product rule: P(AandB) = P(A|B)P(B)

joint probability distribution is a table providing probabilities of all combinations of random variables (sum to 1)
P(A,B) is joint probability of events occuring simultaneously
With product rule (recursively), can express joint probabilities as conditional probabilities:
`P(A,B,C) = P(A|B,C)*P(B,C)`
Independent if have no affect on the other, e.g. P(A|B) = P(A)   

P (Catch | Toothache, Cavity) = P (Catch | Cavity)
We say that Catch is conditionally independent of Toothache given Cavity.
catch conditionally independent of a toothache, if know have a cavity

Identifying independent and conditionally independent variables, can reduce joint probability distribution table size

TODO: Use fringe models for Wumpus world?
A fringe model is a frontier? e.g. possible states that the surrounding boundary could take 

Joint probability distribution specifies probability of every atomic event
➛ Queries can be answered by summing over atomic events
➛ For nontrivial domains, we must find a way to reduce the joint size
➛ Independence and conditional independence provide the tools 

Reinforcement learning is learning by interaction with environment, e.g. action to environment and recieve a state and a particular reward
Different to supervised and unsupervised in that training examples presented one at a time and looking to maximise reward.
(better for non-classification?):
  - Policy:
    How to act in a particular situation
    States are mapped to action probabilities, e.g. π(a|s) 
    Will have predefined actions, e.g. move forward, recharge, etc.
    π\* is optimal policy
  - Reward Function (aim):
    How a state is perceived as a numerical reward
    Want to maximise total reward, not immediate reward.
    So, convey what you want acheived, i.e. focus on end-goal so +1 for winning chess as oppose to subgoal of taking a piece
  - Value Function:
    Cumulative reward agent can expect to recieve in the future from a given state
    So, how good it is for agent to be in a given state in terms of future rewards
    (can calculate by averaging rewards if action chosen 'k' times?)
    (however, for non-stationary, i.e. dynamic environments, better to put more emphasis on more recent rewards; so discount rewards)
    value of state under policy is 'vπ(s)'
    value of taking action under policy is 'qπ(s, a)'
    temporal difference learns action-value function; can be on or off policy

Greedy action exploits current knowledge, non-greedy explores something different from the preferred action to learn.

Episodic means finite, non-episodic means tasks are performed continuously

ideally state should adhere to markov property, i.e. only dependent on current state (however not always possible, e.g. temperature of wheels)

Q-value is immediate reward for action plus discounted value following optimal policy after that action
