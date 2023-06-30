<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Fibonacci matrix used to compute.
Squaring matrix can be done logarithmically, so fibonacci computed logarithmic

Types of proofs to use:
https://edstem.org/au/courses/11846/discussion/1446944

NOTE: polynomial time means n^c (c some constant). so includes n^2, n^3. however not exponential

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
same MST as squaring is monotonic operation (monotonic means preserves order)

not same shortest paths

# Flow Networks
(transportation network, gas pipeline, computer networks)
A flow network is directed graph with each edge positive
Have two distinct vertices; source (start) and sink (end) 
However can have many sources and many sinks (in this case join sources together to single supersource by adding capacities with ∞?)
For vertices with capacities, split into two vertices with connecting edge
1. Capacity constraint:
  Flow through any edge cannot exceed capacity, i.e. weight
2. Flow conservation:
  Flow into vertex equals flow out (no node other than source generates flow; they only distribute)

NOTE: V \ {s, t} means all V that aren't 's' or 't'

## Maximum Flow (Ford-Fulkerson Algorithm) (however Edmonds-Karp is actually used)
(without residual network, i.e. with greedy, will create bottlenecks as ignores 'chains')
Construct residual flow network which shows leftover capacity, as well as reverse virtual capacities (to indicate rerouting flow)
From this determine bottleneck, i.e. smallest of largest path. Then send this bottleneck value.
An augmenting path is this path in residual flow network. We add this onto flow network.
Repeat constructing and adding augmenting paths until '0' edge weight/capacity in residual flow (which equates to removing pipe, so don't have path from S to T)
Terminates: as each run increases edge weight by integer. sum of weights is finite. hence, clearly sum cannot exceed (total flow limited by finite outgoing edges of source) 
Correctness: 

augmenting path is how to reroute, i.e. a path in residual flow network
Once aug. path found, add/subtract both forward and virtual to original flow network.
Then create new residual flow network, and repeat (DFS from source to sink choosing smallest edges?)

sum independent on how you chose the augmentating paths, i.e. can arbitrarily choose augmentating paths
IMPORTANT: distribution may be different, but sum is the same (always maximum)

sum of cut is capacity of all edges leaving S to T (S to T, means across disjoint sets S and T)
TODO: so edges connecting disjoint sets? or more geometric subsections?
flow of cut is flow all edges leaving S to T minus flow of edges leaving T to S

max flow equal to capacity of cut of minimal capacity (minimal cut are all vertices accessible from source)
so, if flow of cut equals capacity of cut, flow must be maximal, capacity minimal (as flow bounded by capacity)
so ford-fulkerson terminates with this flow of this cut:
  * after termination, see that still augmentating paths, just not to T
  * creating a cut for these still existing augmenting paths, see maximal flow out of it

NOTE: first step adds bottleneck, i.e. add smallest capacity  

arrangement of paths affects efficiency.
O(E·f) where f is maximal flow (total number of steps is C)
### Edmonds-Karp (improves by choosing augmenting path with fewest edges O(VE^2))
Faster yet is Dinic's O(V^2E), Preflow-Push O(V^3) (although these are pessimistic, so ok to use Edmonds-Karp)

## Movie Rental, Cargo Allocation
Involve adding super-sources?
Use flow network for chained capacities?


## Vertex Disjoint Paths

