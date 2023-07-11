<!-- SPDX-License-Identifier: zlib-acknowledgement -->

## Shortest Path in DAG (negative)
For positive edge weights in DAG, Djikstra in O(ElogV)
topological ordering allows for recursive operations (i.e. prevents backtracking)
e.g, can say s < v < t in topological ordering
opt(T) is length of shortest path from S to T
As each edge only considered once, O(E)

## Assembly Line Scheduling
multiple subproblems
Find shortest path on workstation k, on assembly line i.
Preceding workstation could be on any assembly line (so exhaustive search)

## Single Shortest Paths (negative)
IMPORTANT: a cycle is not necessarily to itself. could also be chained cycled, i.e. through multiple vertices
Know that shortest path to vertex has no cycles. So, each vertex only appears once in shortest path
Subproblem is shortest distance to 
Bellman-Ford relaxation method? (relaxes the number of edges present in each shortest path)
TODO: so relaxation if recurrence has a limiting parameter, e.g. opt(i, t)
(probably occur if multiple paths?)
O(VE) as for each round, see all edges
argmin() recurrence for obtaining actual vertices on shortest pair

## All Pairs Shortest Path
Floyd-Warshall.
Shortest path with only certain subset of vertices 
Adding vertex only better if it can be inserted into existing collection of vertices and construct a shorter path
O(V^3)

## Bridges Connecting Cities
Bridges will cross if out of order
So, find largest increasing sequence

## Placement of Brackets
Find how many ways can place brackets between symbols i to j making it true 

## Tree Selecting Root
Have simultaneous recursions?
First is to include parent and exclude underlings at depth k
