<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Greedy Proofs
1. Selection Ranges, e.g. (item value, activity selection, ):
   - exchange: adjacent pairs can be swapped like bubble sort until no inversions
   optimal has no adjacent inversions. if no adjacent inversions, then on inversions in whole set.
   IMPORTANT: inversions proof for ordering?
2. Minimal Tree Equalisation:
   - as operating recursively, delay adding maximal length, i.e. root; so minimal
3. Subsequence Determination:
   - exchange: pair swapping
   
# Greedy Solutions
1. Selection Ranges:
   - sort range. select based on one that finishes earliest
2. Minimal Tree Equalisation:
   - recursively work up from leaves. compare children and set edge weight to max. repeat with sub trees
3. Subsequence Determination:
   - find first occurence of letter and delete all preceeding. continue
4. Roof Covering:
   - place board on longest consecutive roofless and continue   
5. Interval Connecting:
   - start with interval with smallest start. 
     for all intervals overlapping with this, pick an interval that ends last
6. Closest Pairings:
   - left-to-right, connect dot with closest opposite coloured dot 
7. Dependent Ordering:
   - choose with minimal sum c + j
8. Activity Selection (largest number of noncompeting):
9. Circular Activity Selection (Overlapping Intervals):
   - TODO: remove jobs crossing midnight. solve remaining same as before
   - then solve separately with each job crossing midnight as starting point 
   - solution is largest between all cases
10. Shortest Hotel Path 
   - IMPORTANT: when vertex has weight, split into two vertices for Djikstra
11. Quickest Increase
   - of available courses, pick one which increases the most and continue
    (greedy states ahead proof)


IMPORTANT: greedy won't work for coin denominations for odd numbers, e.g. 4c, 3c and 1c


matching in bipartite is vertex disjoint, i.e. edges can't connect multiple vertices

## Max Bipartite Matching
max flow of network with all edges weight 1

## Job Centre
NOTE: for problems matching 'person' to 'job' thought of as a bipartite graph
to construct this graph have O(p·j·q) (q is qualification count)
then find max matching with Edmonds-Karp = O(V·E^2)
E = nm + n (all person to source) + m (all job to sink)

IMPORTANT: when creating graph, incorporate say 'defective' squares

# Dynamic Programming
We want overlapping subproblems, so can reuse later in recursive construction
1. Define subproblem (hardest part). Often by adding restriction to subproblem, makes combining easier?
2. Recurrence relation (how subproblems combine)
3. Base case

## Longest Increasing Subsequence

