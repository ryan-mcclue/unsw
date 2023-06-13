<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Fibonacci matrix used to compute.
Squaring matrix can be done logarithmically, so fibonacci computed logarithmic

## Interval Joining
Find shortest distance between intervals and join on them iteratively

## Minimal Number of Coins
Contrapositive Proof: Violating greedy, we pick lower denominations
i.e. have value of at least $2, but don't use a $2, hence violating optimality of solution

## Items for Sale
TODO: look over in more_problems.pdf
Choose min(a, b).
Also have differences, i.e. max(a, b) - min(a, b)? 

2nlogn = nlogn

## Squaring Edge Weights
TODO: same MST as squaring is monotonic operation, i.e. preserves order?
not same shortest paths

# Flow Networks
A flow network is directed graph with each edge positive
Have two distinct vertices; source (start) and sink (end)
1. Capacity constraint:
  Flow through any edge cannot exceed capacity, i.e. weight
2. Flow conservation:
  Flow into vertex equals flow out (no node other than source generates flow; they only distribute)

## Maximum Flow
Construct residual flow network which shows leftover capacity, as well as reverse virtual capacities (to indicate rerouting flow)
From this determine bottleneck, i.e. smallest of largest path. Then send this bottleneck value.
An augmenting path is this path in residual flow network. We add this onto flow network.
Repeat constructing and adding augmenting paths until '0' edge weight/capacity in residual flow
Terminates: as each run increases edge weight by integer. sum of weights is finite. hence, clearly sum cannot exceed
Correctness: 
