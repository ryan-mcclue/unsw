## Data Structures:
* Orientations enum:
  Provides a readable encoding of a bridge's orientation on the map.
  NULL indicates no bridge is present.
* Directions enum:
  Encodes a connected bridge's direction from the perspective of an island.
  Opposite directions are encoded as the bitwise and of each other.
  This allows a bridge's direction to be inverted from the perspective of the destination island.
* Node class:
  Encodes a location on the map.
  Can either be an island or a possible bridge location.
  They can be told apart as a bridge will have 0 for number of required bridges.
  By combining information, can have one node type to simplify map representation.
  Fields for an island node:
    - Number of connected bridges
    - Number of the currently connected bridges
    - Number of bridges connected in a particular direction
  Fields for a bridge node:
    - Orientation of bridge
    - How many bridges currently containing
* NeighbourNode class:
  From the perspective of a source node, encodes a destination node that could be connected to it.
  The direction field indicates the direction the destination node is facing from the source node.
* State class:
  Encodes map. Stores number of rows, columns and a node array of `row*columns` size.
* Move class:
  Encodes a move to be made on the state, with x and y representing the source node that the move will be made on.
  The move contains an array of bridge amounts, representing the number of bridges to connect to the corresponding neighbour node array.

## Program:
  The map is read line by line from stdin. 
  Each character of the line is converted to a node that goes into the state object.
  Firstly, all definite moves are explored. A definite move is:
  1. The node is only connected to a single neighbour, in which case all its bridges must connect with it.
  2. Summing all possible bridge connections to neighbour nodes equals nodes bridge target. 
     In this case, each neighbour should have the maximum number of bridge connections.
  Once all definite moves are explored, a backtracking algorithm is employed.
  It is a recursive DFS implementation.
  Reasons DFS was chosen:
    - Knew no cycles, so would not get stuck
    - There is no optimal solution, so sub-optimal limitations not a concern.
      Get added bonus of linear space complexity over BFS.
  For each island:
  1. All effective neighbour nodes are found.
     An effective neighbour is one that is not blocked by a bridge and could take more bridge connections.
  2. From the effective neighbours nodes, generate all possible moves. 
     A move is what combination of bridges to neighbour nodes could satisfy the target bridge amount.
  3. Order the moves based on the move that has the neighbour node with smallest target getting the most connections.
     This is because a smaller target node will be more restrictive and hopefully minimise depth of recursion.
  4. If the move is valid, apply it and recurse on it, i.e. explore this option.
     If exploring this option does not yield solution, undo the move.
  Base cases:
    - Recieve coordinates one past the dimensions of the map, know have solved, return true.
    - No bridges in any direction can be added to the island, return false.
  The state object is finally printed, representing a solution.
