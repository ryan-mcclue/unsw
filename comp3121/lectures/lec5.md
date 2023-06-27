<!-- SPDX-License-Identifier: zlib-acknowledgement -->

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

WITHOUT INIFINITE NUMBER OF OBJECTS:
now 2D table size (num objects * capacities)
so, opt(i, k) where maximum value using up to 'i' units of weight using only 'k' items

## Balanced Partition
By creating a subset of sum S/2, we will ensure that both subsets are as close to possible to S
