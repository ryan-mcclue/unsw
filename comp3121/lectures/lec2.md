<!-- SPDX-License-Identifier: zlib-acknowledgement -->
multiplication of polynomials faster than large numbers? (don't need as many large integer multiplications, as are computing coefficients)
multiplying two polynomials of degree 2 gives degree 4
splitting into 3 sections with polynomials faster than Karatsuba

although asymoptotically faster slicing into smaller pieces, constants (i.e. coefficients) grow very fast, e.g. 1million·n or 10^8·n etc.
so, most always know what constants are. 
not enough to just look at asymptotic to say faster than another
(this follows for divide-and-conquer, i.e. faster for small lists if do linearly)

TODO: warden puzzle write-up

eigenvector used to google page rank algorithm?

## Greedy Method (lots of combinatorial problems?)
chooses choice which assumes is best at that time (dynamic programming is more global?)
greedy most useful technique for solving problem? 

## Activity Selection (pick largest number of non-conflicting activities):
greedy with respect to time, i.e picking shortest activity is suboptimal
greedy with respect to least conflicts is suboptimal
working left to right, greedy with respect to earliest finishing time is optimal
*Greedy Proof 1*: proof exchange argument (show that any allegedely better solution can be morphed into our greedy solution)
we know that at any stage, any better solution activity can be replaced with greedy solution
as anything on right we know won't conflict with (as earlier)
O(nlogn) as sort by earliest finishing time

## Petrol Stations:
pick furthest petrol station from where at
*Greedy Proof 2*: proof greedy stays ahead (no other solution beats greedy at any stage)

## Cell Towers:
Start from first house not covered. place tower 5km from that house. repeat
proof exchange: any solution can be shifted

## Minimising Job Lateness:
sort jobs in increasing order of deadlines

suppose alternative solution that pick out-of-order
show that swapping will increase, i.e. will be more optimal
(i.e. swapping adjacent inverted jobs reduces lateness)

## Tape Storage:
pick where probability/file-size is smallest
proof: show that optimal solution does not have inversions (subtract lists)

## Interval Stabbing:
stab in the interval that ends the earliest at this place

## Fractional Knapsack:
Take most valuable per unit weight. However, if don't fill entire knapsack; suboptimal
So, trial and error

TODO: after lectures do practice problems (as reinforce lecture problem solving)

TODO: know what type of greedy to use particular proof

NOTE: seems that for greedy just sort on desired trait?

## Huffman Code:
For efficient encoding scheme, would want to give frequent characters to have short codes,
and less frequent longer codes
To allow for coding identify, ensure that no code has same prefix (prefix codes)
Short branches frequent symbols
Long branches infrequent symbols

## Tsunami Warning:
(NOTE: for nested-connections, use graph over simply sorting and greedy?)
strongly connected component in graph is where can travel from one vertex to another and back 
to find these strongly connected components:
BFS finds all vertices acessible from a particular vertex
So, use this to create graph 1
Then, create another graph with edges reversed
Now, look at intersection of vertices to create strongly connected component
Repeat for all vertices
Condensation graph is graph of all strongly connected components (in effect, set of super-towers)
Find strongly connected component that doesn't have an incoming edge. Put sensor there
Then remove component and repeat
Backtracking search viable as condensation graph is acyclic
O(V(V + E))

## DAG allows for Topological Sort (so could be used to determine if cycle exists):
Take list of all vertices that are empty and add
Then for all vertices with zero in-degrees, i.e. no incoming edges, add 
O(V + E)

## Single Shortest Path to all Vertices:
Djikstra's greedy algorithm for DAG
Claim: Picking path that shortest, will find total shortest path
Contrapositive: Assume another point exists that is shorter path.
O(n^2)
most efficient uses vertices kept in augmented min-heap (i.e. heap element is a pair, so sorted on distance, also contain original vertex identifier) as oppose to array
O(mlogn)

## Minimum Spanning Tree:
connects all vertices with smallest weight of edges
Prims algorithm similar to Djikstras
Kruskal algorithm builds up forest (O(mlogn))
Order vertices by edge weight (is this topological sort?). Add vertex only if doesn't introduce cycle
(example of backtracking algorithm? common in graph problems?)
Want quick way to determine if two ends of edges belong to same tree to avoid a loop
Efficient implementation uses Union-Find data structure to store connected components we have built up and perform cycle detection on
O(n^2logn)

## K-Clustering of Maximum Spacing
Kruskal for MST tries to join subtrees with smallest edges. 
We do this until whole forest becomes single tree
Here, we stop when we reach k many subtrees, i.e. k distinct labels
O(n^2logn)

TODO: padlock box sending


greedy won't work if local and global maximas?
