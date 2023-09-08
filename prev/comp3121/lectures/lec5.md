<!-- SPDX-License-Identifier: zlib-acknowledgement -->

TODO: implement divide-and-conquer in code etc.

Dynamic programming can efficiently look at all options at a stage. More global than greedy (use if greedy doesn't work?)
DP recursion is more backtracking?

# Dynamic Programming
We want overlapping subproblems, so can reuse later in recursive construction
1. Define subproblem (hardest part). Often by adding restriction to subproblem, makes combining easier?
   e.g. longest subsequence MUST end in index i
2. Recurrence relation (how subproblems combine)
3. Base case

Must choose subproblems that overlap in recursion tree

## Longest Increasing Subsequence (backtracking)
For each index look back and see what subsequences can it extend, i.e. what previous number is it larger than
If found, increment count of previous subsequence end
This equates to finding opt(i), which is maximum length of increasing subsequence that ends in i
base case is opt(i) = 1
Once solved all subproblems, pick best solution amongst these
NOTE: inside array of opt(i), can store index of predecessor

O(n^2)

## Largest Duration Activity Selection (backtracking)
For each activity look back and see the longest duration count activity it can extend
If found, increment duration count 

Sort then O(n^2)

Proof (cut-and-paste): if truncated subsequence optimal

## Making Change (construction problem) 
Create table with C many slots (therefore large table/recursion amount)?
As solving for every amount smaller than C?

O(number of coins * number of denominations)

## Knapsack 
Want to pick largest value items into capacity
Solve for all knapsacks with capacity 1 up to C (therefore, large recursion)

For each capacity subtract a particular item. 
As this is smaller than current capacity, we know what optimal solution for this will be in our table.
Check this for all items at that stage and pick optimal and continue

Recursion depth is C, and each stage cost is n (number of kinds of objects)
IMPORTANT: not polynomial

WITHOUT INFINITE NUMBER OF OBJECTS:
now 2D table size (num objects * capacities)
so, opt(i, k) where maximum value using up to 'i' units of weight using only 'k' items

## Balanced Partition
By creating a subset of sum S/2, we will ensure that both subsets are as close to possible to S

## Matrix Chain Multiplication
Matrix multiplication each resultant element is dot product of row with column
So, O(n·m·p), i.e. rows x columns x row
So, nxn · bxb gives nxb
Recursive step is an exhaustive search
Determine splitting point and two portions to multiply, e.g. opt(i, j)
O(n^3)

## Longest Common Subsequence
Truncate subsequences. If last element in each is same, peel off element in one and check.
IMPORTANT: when defining subproblems, state the ordering of solving subproblems (typically lexicographically, as dependency i-1 solved before i)
TODO: dynamic solutions for opt(x, y), i.e. truncating subsequences

## Shortest Common Supersequence
Find LCS, then insert letters missing from two subsequences

## Edit Distance/Measure of Similarity
Assuming deletion/insertion are unit costs, then the minimal number of operations to transform A to B is Levenshtein Distance

Subproblem: opt(i, j) minimum cost of transforming A[0...i] into B[0...j] (overall solution is opt(n, m))
Recurrence (i.e. how to backtrack in table): opt(i, j) = min(opt(i - 1, j) + deletion) or min(opt(i, j - 1) + insertion)
Base case: opt(i, 0) = cost to delete all characters
Complexity: nm subproblems, O(nm)

## Maximising an Expression 
i.e. find optimal placing of brackets for expression, e.g: 1 + 4 * 10 + 1 - 7 * 1 + 23
TODO

## Turtle Tower

## Integer Partitions
How many ways can 1 integer be split into partitions of smaller integers that add up to it
nump(i, j) number of ways to partition j, so that each part smaller than i
Perform relaxation on i, i.e. alter value of i:
nump(i, j) = nump(i-1, j) + nump(i, j - i)

## Shortest DAG Path
Djikstra's fails for negative edges 
Topological ordering of vertices, so that all edges go from left to right
This allows to do recursion in efficient way, and build up subproblems from each vertex
