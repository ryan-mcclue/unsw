<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Assignment 1 – Search and Constraint Solving

1a) NOTE: G (path length), N (states expanded)

Mem - out of global stack

|             |start10  | start12 | start20 | start30 | start40 |
|-------------|---------|---------|---------|---------|---------|
| **UCS**     |10,2565  |Mem      |Mem       |Mem      |Mem      |
| **IDS**     |10,2407  |12,13812 |20,5297410|Time     |Time     |
| **A\***     |10,33    |12,26    |20,915    |Mem      |Mem      |
| **IDA\***   |10,29    |12,21    |20,952   |30,17297 |40,112571|

1b)
    Is it complete? An algorithm is complete if it terminates for any input.
    Is it optimal? We say that an algorithm is optimal if it returns the optimal path to the goal, provided that at least one goal state is reachable from the start state. If more than one state passes the goal test, we want the lowest-cost path among all the paths leading to any goal.
    What’s the algorithm’s time complexity?
    What’s its space complexity?
  (I) [ucsdijkstra]
  djikstra implementation of ucs with no goal state, i.e. will find for all paths 
    
  (II) [ideepsearch]
  'd' is the length of the shortest path to a target node
  'b' maximum number of children in graph
  'm' longest path between any two nodes in graph
  time: O(b^d) 
  space: O(bd)
  
  (III) [astar]
  informed

  (IV) [idastar]
  informed

TODO: In relation to time (and other features) are we giving a numerical answer like O(b^n), or just explaining in layman terms like only returns one result so more time efficient?


