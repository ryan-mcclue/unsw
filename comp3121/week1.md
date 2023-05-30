<!-- SPDX-License-Identifier: zlib-acknowledgement -->

but the general proof ideas (contradiction, induction etc.) are very useful so I would focus on them.

priority queue typically implemented as a heap, but could also be implemented in say a splay tree

about designing and proving correctness of algorithm
so, this is more computer science (as engineers implement from this paper)
mathematical reasoning required to proove, e.g. justify that sorting algorithm will sort?
practical problem solving, i.e. learning algorithm design techniques (divide-conquer, greedy, dynamic, etc.)
gain skill, not necessarily knowledge

informal algorithm is using words rather than pseudocode? 

mathematical proof only required if non-obvious
sometimes not clear will enter infinite loop
sometimes not clear will run in exponentially many steps
sometimes not clear will produce desired solution

want to show algorithm:
terminates (hospital cannot make more than one offer to a doctor)
runs in reasonable time (each hospital can make at most n offers)
produces correct output 

proof of contradiction popular, e.g. assume that ...


n! ≈ (n/e)^n


the merge sort proof is an informal proof by induction?
inductive step is assuming previous step is sorted and then this bubbles up
in each depth of recursion, have O(n) merge step



in-person inspera (done in a CSE lab; so is it on a lab computer or your own computer?)
(cormen, leiserson et. Introduction to Algorithms 'bible of algorithms', i.e. reference manual for later work)
