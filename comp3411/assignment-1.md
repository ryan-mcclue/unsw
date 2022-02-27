<!-- SPDX-License-Identifier: zlib-acknowledgement -->

# Assignment 1 – Search and Constraint Solving

1a) NOTE: G (path length), N (states expanded)

Mem - out of global stack

|             |start10  | start12 | start20   | start30 | start40 |
|-------------|---------|---------|---------  |---------|---------|
| **UCS**     |10,2565  |Mem      |Mem        |Mem      |Mem      |
| **IDS**     |10,2407  |12,13812 |20,5297410 |Time     |Time     |
| **A\***     |10,33    |12,26    |20,915     |Mem      |Mem      |
| **IDA\***   |10,29    |12,21    |20,952     |30,17297 |40,112571|

1b)
  All the algorithms are complete and optimal and have time complexity of O(b ^ m)

  uscdijkstra is essentially a BFS search with weighted edges.
  As such, it shares BFS's exponential space time complexity of O(b ^ m).
  This is inefficient for large problems and can be seen with prolog generating a 'Mem - out of global stack' for start12 ... start40

  IDS is a repeated DFS depth-limited search. 
  As such, it has much better space time complexity than ucsdijkstra of O(b·m).
  This can be seen with it being able to compute start10 .. start20
  However, the repeated search means for goals close to the target, it is slower than ucsdijkstra which can be seen in start10
  IDS is an uninformed search and therefore expands are large number of unecessary nodes.
  The consequence of this is seen with the algorithm 'timing out' from start30 ... start40

  A\* is essentialy an informed ucsdijkstra.
  This use of a heuristic means it is able to expand less nodes than ucsdijsktra and IDS.
  As a result, A\* computes more solutions than ucsdijkstra, e.g. start10 ... start20 
  However, like ucsdjikstra it has exponential space time which results in 'Mem' for start30 ... start40

  IDA\* combines the aforementioned benefits of linear memory efficiency of IDS and the informed search of A\*.
  It's therefore able to compute solutions to start10 ... start40
2)
|            | start50       | start60        | start64         |
|------------|-------------  |----------------|-----------------|
| **IDA\***  | 50 , 14642512 | 60 , 321252368 | 64 , 1209086782 |
| 1.2        | 52 , 191438   | 62 , 230861    | 66 , 431033     |
| 1.4        | 66 , 116174   | 82 , 3673      | 94 ,188917      |
| 1.6        | 100 , 34647   | 148 , 55626    | 162 , 235852    |
| **Greedy** | 164 , 5447    | 166 , 1617     | 184 , 2174      |

Greedy finds suboptimal solution as indicated by exceeding the minimum number of moves described in the starting position name
