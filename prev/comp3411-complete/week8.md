<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Robot makes an intelligent perception to an action (recognise and plan)
Have Robot Operating Systems.
As typically moving, frame of reference changing; e.g. world may be of fixed dimension and reference is offset in those dimensions
Egocentric is from observer's POV. Allocentric based on fixed reference points. 

Evolution based reinforcement learning is model-free, e.g. OpenAI evolution strategies.
AlphaGo was model based.

TD-Learning (temporal difference; q-learning) is reinforcement learning.

Use neural network to learn best static evaluation for alpha-beta? (could introduce expectimax if stochastic)
this learns via backpropagation
however, require a (target - value). so, how do we find a better estimate for current position?
  1. Learn from expert human plays (humans might not be best at game, so learning from self-play might be preferable)
  2. TD-learning (good for stochastic; does not rely on knowing world model or rules of game)
  3. Learning with tree search (good for deterministic), e.g. TD-root (TD knowing world model), MCTS (good for high branching factor) 
