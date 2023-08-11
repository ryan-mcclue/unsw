<!-- SPDX-License-Identifier: zlib-acknowledgement -->
https://courageous-postbox-384.notion.site/COMP3121-Tutorials-7490cbbb823044fcac4453661746ab42

`f(n) = O(g(n))`, if `f(n)/g(n) <= C` or `lim∞ f'(n)/g'(n) = 0` *(limit asymptotic theorem)*
`f(n) = Ω(g(n))`, if `f(n)/g(n) > C` or `lim∞ f'(n)/g'(n) = ∞`
`f(n) = θ(g(n))`, if `O(n) = Ω(n)` or `lim∞ f'(n)/g'(n) = 0`

TODO: LOG-RULES
TODO: arithmetic/geometric sums

TODO: data-structures and algorithms time complexity
Topological (vertices connected left to right): `O(|V| + |E|)` 
Djisktra (shortest path to all vertices): `O(|V^2|)`
Prims (minimum spanning tree): `O(|V^2|)`
BFS (find all vertices accessible): `O(|V| + |E|)` 
Heap:
SelfBalancingTree:

#### Divide and Conquer
`T(n) = a·T(n/b) + f(n)`, *a = num-subproblems*, *b = size-subproblems*
critical: `n^(logbᵃ)`, `< θ(n^(logbᵃ))`, `= θ(n^(logbᵃ)·log2ⁿ)`, `(> and a·f(n/b) <= c·f(n)) θ(f(n))` 
TODO: binary-search monotonicity, upper/lower bounds
**Algorithm**
1. Recursively divide into two subarrays of approximately equal parts. Find distinct cards in the first `k/2` and last `k/2`.
2. Merge the results of 2 subarrays by checking through each card one by one in both halves to get a subarray with distinct cards.
3. Base case: for `n=1` students, a single collection contains distinct cards
**Induction**
For base case of `n=1`, we know a single collection has distinct cards. 
Assume this works for `n=k`. 
For `n=k+1`, by problem definition, merging two collections will always produce a collection of distinct cards. 
So, merging two collections of `n=k` will produce a distinct collection at `n=k+1`.
#### Greedy
**Stays-Ahead**
1. Let greedy solution be G = (g1, g2, g3, ..., gn) where gi represents a particular rod. 
   Let an alternative supposed optimal solution be O = (o1, o2, o3, ..., on)
2. Base case is welding the 2 shortest rods. 
   Welding g1 + g2 will yield the absolute shortest welded rod of absolute minimal cost of any 2 rods. 
   Therefore, welding g1 + g2 costs no more than welding o1 + o2.
3. Assume that welding rods up to gk−1 costs no more than welding rods up to ok−1  
4.  As stated previously, the cost of the resultant
rod from gk−1 welds is no more than ok−1. Therefore, gk−1 + gk cannot cost any
more than ok−1 +ok as the length of ok (and by definition the cost increase) cannot
be greater than that incurred by welding gk. As a result, since O is arbitrary, G
must be optimal
ALTERNATE: If these rods were not present at this location in O, then they must appear closer to the centre of O. 
TODO: **Contradiction**
Moreover, since the greedy algorithm deletes vertices from G, it must
have arrived at graphs that contain H as a subgraph. In particular, the greedy algorithm
must arrive at H′ before H
Suppose that there exists an alternative solution that deletes a smaller set of
vertices D = (v0, v1, ...) at this point than our solution. Therefore, there must exist
at least one vertex vi in our solution not in D. For vi to not have been deleted, it
must not be adjacent to at least k vertices. However, our algorithm only deletes
vertices that are not adjacent to less than k vertices, i.e. wouldn’t delete vi. This
contradicts assumption that D represents a smaller optimal solution. Therefore,
algorithm is optimal.

  terminates
  correctness
  time-complexity

#### Flow
`O(|V| + |E|)`, `O()`

dp
