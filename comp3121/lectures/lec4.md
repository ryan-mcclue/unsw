<!-- SPDX-License-Identifier: zlib-acknowledgement -->

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

