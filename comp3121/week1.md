<!-- SPDX-License-Identifier: zlib-acknowledgement -->
## Introduction
Course more computer science as about designing and proving correctness of algorithm
Want to gain problem solving skills and algorithm design techniques, e.g. divide-conquer, greedy, dynamic, etc.

A informal algorithm is solved in prose rather than pseudocode

Big-Oh (asymptotic upper bound)
f(n) = O(g(n)), i.e. f(n) grows at most g(n)
Omega (asymptotic lower bound)
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

Gale-Shapely Algorithm (Stable Matching Problem):
1. Quadratic: each hospital can make at most n offers and there are n hospitals
2. Terminates: each hospital cannot make more than one offer to a doctor
3. Contradiction (good proof to start with?): 
   Assume produces non-stable match (h, d), (h', d')
   h would offer to d' first
   d' would reject if already at higher. we know this didn't happen
   d' would accept and later recind. would not recind for lower


The general rule of thumb is that algorithms introduced in this course (in either the lectures, tutorial, problem sets) does not need citation - 
simply citing which slide / problem set number (question #) is typically enough

TODO: in-person inspera (done in a CSE lab; so is it on a lab computer or your own computer?)
(cormen, leiserson et. Introduction to Algorithms 'bible of algorithms', i.e. reference manual for later work)
