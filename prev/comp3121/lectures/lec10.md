<!-- SPDX-License-Identifier: zlib-acknowledgement -->
For finding actual elements for DP, would define a new subproblem, e.g. prev(i) = argmax(...)

## Make Change (Placing Objects)
min(amount) = minimum( min(amount - coin_value) for-all-coin-values ) + 1
IMPORTANT: O(nC): not polynomial, exponential in log(C) as C can be represented in log(C) bits
NP-Hard problem

Similarly, for knapsack problem, length of recursion is length C (so not polynomial?)
max_value(weight) = maximum(max_value(weight - item) + item_value)
(as for all values at each subproblem, is an exhaustive search)
IMPORTANT: this assumes unlimited supply of items 

## Partitions
num(i, j) number of paritions of j in which no part exceeds i
num(i, j) = num(i - 1, j) + num(i, j - i)

## Turtle Stack
order turtles by increasing strength + weight
