<!-- SPDX-License-Identifier: zlib-acknowledgement -->

IMPORTANT: 
If linear, them are going from 0-n, or i-n,j-0 etc.
For opt() might have multiple circumstances once of which involves 'peeling' off a letter
For opt(), consider finding up till a value (may have to sort lists first so that 0..i makes sense)
Might have i for set 1 and j for set 2 combining to i+j in set 3

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

## Items into Bins
opt(num_s1, num_s2)
num_s1_objects = bin_cap / s1
remaining_s2_objects = (C - num_s1_objects * s1) / s2
opt(i, j) = min(opt(i - num_s1_objects, j - remaining_s2_objects))
run for all values of K, so exhaustive search

## Activity Selection
opt(i): max profit choosing activities up to a_i

max{opt(j) : f_j < s_i (this indicates no conflicting)} + p_i

argmax (index for which result is maximum)

## Knapsack Problem
IMPORTANT: dynamic programming required when greater number of objects than what is available to be placed
Items with weight and cost into bag.
Problems can be refactored into this, e.g: 
job takes t trucks and gives d dollars; have total T trucks

## Dam allocation
Find maximum number of dams that end on dam_i
opt(i) = 1 + max{opt(j): dam_i - dam_j > max(dam_i_prop, dam_j_prop), j < i}

## Board Square Moves
num_ways = {ways(x - 1, y) if opt(x - 1, y) > opt(x, y - 1)}
in otherwords, if optimal left, then increment ways by 1
increments ways by 2 if either way the same

## Palindrome
Have range i, j. Move forward by i, backwards by j
opt(i, j):
  1. If end points match, longest palindrome in between + 2
  2. If end points don't match, peel letter of both i and j and max palindrome between them

## Partitions
numparts(i, j): numparts(i - 1, j) + num(i, j - k) 
equivalent to finding numparts less than k and numparts with k

##
opt(column, pattern) = score(column, pattern) + max(opt(column - 1, compatible_pattern))

## Interleaved
Is i+j bit of Z string same as ith bit in A or jth bit in Z

## Workers
opt(i, j): days failed up to day i if have j workers
