<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Introduction
Course more computer science as about designing and proving correctness of algorithm
Want to gain problem solving skills and algorithm design techniques, e.g. divide-conquer, greedy, dynamic, etc.

A informal algorithm is solved in prose rather than pseudocode

Big-Oh (asymptotic upper bound, i.e takes at most as long)
f(n) = O(g(n)), i.e. f(n) grows at most g(n)
Omega (asymptotic lower bound, i.e takes at least as long)
f(n) = Ω(g(n)), i.e. f(n) grows at least g(n)
Theta (same asymptotic growth rate)
f(n) = θ(g(n))

Proof ideas:
Induction (true for case k, true for case k+1 etc.) (might involve partial/infinite sums)
Contradiction

Mathematical reasoning required to proove only if non-obvious:
  * Valid time complexity assertion
  * Is finite, i.e. won't enter an infinite loop
  * Produce desired solution, e.g sorting algorithm will sort

Merge Sort:
1. Loglinear: logarithmic recursion depth, linear merge at each depth
2. Terminates: subarray length will always reach 1
3. Induction: merging sorted arrays at any depth k will always create sorted array

Factorial time complexity is exponential, i.e. n! ≈ (n/e)^n

Stable Matching Problem (Gale-Shapely Algorithm):
1. Quadratic: each hospital can make at most n offers and there are n hospitals
2. Terminates: each hospital cannot make more than one offer to a doctor
3. Contradiction (good proof to start with?): 
   Assume produces non-stable match (h, d), (h', d')
   h would offer to d' first
   d' would reject if already at higher. we know this didn't happen
   d' would accept and later recind. would not recind for lower

TODO: n-thieves write up

## Divide and Conquer (useful to increase speed from say quadratic to loglinear)
counterfeit coin puzzle
array inversion count (merge sort variant)

estimation of growth rate of recurrences

order statistics is position in array if sorted.
so, used for problem like find second most populous
has linear time?


## Textbook Chapter 1
Competitive Facility Location Problem

Draw as a graph if some connection and value?

Interval Scheduling ()
Each node interval, edge is if they overlap
(want to find independent set; which is NP-complete, i.e. no known efficient algorithm)

Bipartite Matching Problem

PSPACE-complete is harder than NP-complete
This is because a 'short proof' of a solution is difficult

When a greedy algorithm can be shown to ﬁnd an optimal solution for all instances of a problem, it’s often fairly
surprising. We typically learn something about the structure of the underlying
problem from the fact that such a simple approach can be optimal.

Instead, we employ a technique, dynamic programming, that builds up the
optimal value over all possible solutions in a compact, tabular way that leads
to a very efﬁcient algorithm.


TODO: in-person inspera (done in a CSE lab; so is it on a lab computer or your own computer?)
(cormen, leiserson et. Introduction to Algorithms 'bible of algorithms', i.e. reference manual for later work)
