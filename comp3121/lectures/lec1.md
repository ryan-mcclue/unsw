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

NOTE: When calculating asymptotic relation, ignore constants and lower factors

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

TODO: n-thieves write up (start)
TODO: handshake write up (end)

## Divide and Conquer (useful to increase speed from say quadratic to loglinear)
Counterfeit Coin Puzzle:
* Divide coins into n piles
* Finding which pile's mass is different to the others says this pile has counterfeit
* Then recursively divide that pile until 1 coin remaining

Array Inversion Count:
TODO: array inversion count (merge sort variant)

Divide-and-conquer method for large integer multiplication splits number into halves `a = a1·2^(n/2) + a0`
Karatsuba trick says we don't need all 4 products, only 3
Left-shift mask can be represented mathematically as `2^(n)`

For digit multiplication (non-Karatsuba): `T(n) = 4·T(n/2) + cn`
Evaluating T(n/2) and inserting into T(n) and so we obtain `T(n) = n^2·(c + 1) - cn = θ(n^2)`

Master Theorem allows us to estimate growth rate without explicitly solving recurrences.
Divide and conquer growth rate: `T(n) = a·T(n/b) + f(n)`, e.g. merge sort: `T(n) = 2·T(n/2) + cn`
* a = number of subproblems
* b = size of subproblems
* f(n) = subproblem combination overhead
Critical polynomial is `n^(logbᵃ)`
1. f(n) < critical polynomial, then: `θ(n^(logbᵃ))`
  * 4·T(n/2) + n
  * critical polynomial = n^(log2⁴) 
  * n < n^2
2. f(n) = critical polynomial, then: `θ(n^(logbᵃ)·log2ⁿ)`
3. f(n) > critical polynomial, and `a·f(n/b) <= c·f(n)`, then: `θ(f(n))`

NOTE: logarithms of any base have same growth rate


order statistics is position in array if sorted.
so, used for problem like find second most populous
has linear time?


redefine median as kth smallest value in an unordered set 
i.e. n/2 values smaller than it
pivot just means value to which putting elements to the right or left of

median of medians, divide list into blocks each of size 5
sort these lists. consider this linear as 5 elements very quick
put median of these lists into another list
sort that list and get median.
this is now pivot, put all elements in original list < to left of pivot and > right of it
based on index of pivot, we can see if need to recurse on left or right side


find median of each 5 block than
find true median of these n/5 elements recursively

https://edstem.org/au/courses/11846/discussion/1418436
https://edstem.org/au/courses/11846/discussion/1422278


TODO: petrol station problem write up (end)

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
