<!-- SPDX-License-Identifier: zlib-acknowledgement -->

exam design questions:
1. divide-conquer or greedy
2. max-flow
3. dp

## DC: Counting Inversions
user2_ranks;

top, bottom = user1_ranks;

any merge sort variant: 2T(n/2) + cn

## Order statistic (doable in linear time!)
Order statistic is generalisation of median.
So for `1<k<n`, finding how many elements larger than it. so if k = n, is max

1. groups of 5 elements.
2. order elements in groups
3. for middle group find median for pivot. 
take all groups whose median is larger than pivot put them on right hand side of array
if number of elements smaller than pivot is median, then return
if <, recurse on ith smallest for pivot
else, recurse on (i - k) smallest for pivot
(recurse like quicksort; so quicksort is divide-and-conquer?) 
- partitioning like this ensures each part at least 3/10 smaller and larger, 7/10 rest?

## Activity Selection
Greedy exchange works more often? So first, see for every stage, can exchange allegedely better solution part to greedy

## Cargo Allocation (grid)
Vertices for rows and columns, cells edges
Other times vertices are cells, and edges might be rows/columns/diagonals etc.
IMPORTANT: max-flow naturally defines a min-cut

## DAGs (think about topological sort)
Topological sort has all edges from left to right. Allows for DP in linear time with respect to number of edges
So for shortest path, can do: min(opt(v) + weight(v, t))

## LCS (if exists a long one, then high degree of similarity)
opt(i, j), one index for each list
Consider cases:
1. endpoints match
2. endpoints don't match, peel one off

## Tree Structure
Consider two subproblems:
I(i) = optimal weight of subtree if root included
E(i) = optimal weight of subtree if root not included
solution = max(I(i), E(i))
