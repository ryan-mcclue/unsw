#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

#################################################################
## QUESTION ANSWER ##############################################
#################################################################
## DATA STRUCTURES:
# * Orientations enum:
#   Provides a readable encoding of a bridge's orientation on the map.
#   NULL indicates no bridge is present.
# * Directions enum:
#   Encodes a connected bridge's direction from the perspective of an island.
#   Opposite directions are encoded as the bitwise and of each other.
#   This allows a bridge's direction to be inverted from the perspective of the destination island.
# * Node class:
#   Encodes a location on the map.
#   Can either be an island or a possible bridge location.
#   They can be told apart as a bridge will have 0 for number of required bridges.
#   By combining information, can have one node type to simplify map representation.
#   Fields for an island node:
#     - Number of connected bridges
#     - Number of the currently connected bridges
#     - Number of bridges connected in a particular direction
#   Fields for a bridge node:
#     - Orientation of bridge
#     - How many bridges currently containing
# * NeighbourNode class:
#   From the perspective of a source node, encodes a destination node that could be connected to it.
#   The direction field indicates the direction the destination node is facing from the source node.
# * State class:
#   Encodes map. Stores number of rows, columns and a node array of `row*columns` size.
# * Move class:
#   Encodes a move to be made on the state, with x and y representing the source node that the move will be made on.
#   The move contains an array of bridge amounts, representing the number of bridges to connect to the corresponding neighbour node array.
# 
# ## PROGRAM:
#   The map is read line by line from stdin. 
#   Each character of the line is converted to a node that goes into the state object.
#   Firstly, all definite moves are explored. A definite move is:
#   1. The node is only connected to a single neighbour, in which case all its bridges must connect with it.
#   2. Summing all possible bridge connections to neighbour nodes equals nodes bridge target. 
#      In this case, each neighbour should have the maximum number of bridge connections.
#   Once all definite moves are explored, a backtracking algorithm is employed.
#   It is a recursive DFS implementation.
#   Reasons DFS was chosen:
#     - Knew no cycles, so would not get stuck
#     - There is no optimal solution, so sub-optimal limitations not a concern.
#       Get added bonus of linear space complexity over BFS.
#   For each island:
#   1. All effective neighbour nodes are found.
#      An effective neighbour is one that is not blocked by a bridge and could take more bridge connections.
#   2. From the effective neighbours nodes, generate all possible moves. 
#      A move is what combination of bridges to neighbour nodes could satisfy the target bridge amount.
#   3. Order the moves based on the move that has the neighbour node with smallest target getting the most connections.
#      This is because a smaller target node will be more restrictive and hopefully minimise depth of recursion.
#   4. If the move is valid, apply it and recurse on it, i.e. explore this option.
#      If exploring this option does not yield solution, undo the move.
#   Base cases:
#     - Recieve coordinates one past the dimensions of the map, know have solved, return true.
#     - No bridges in any direction can be added to the island, return false.
#   The state object is finally printed, representing a solution.

import sys

from dataclasses import dataclass, field
from typing import List
from enum import Enum

class Directions(Enum):
  NULL = 0
  RIGHT = 0b0011
  DOWN = 0b10
  LEFT = 0b1100
  UP = 0b01

class Orientations(Enum):
  NULL = 0
  VERTICAL = 1
  HORIZONTAL = 2

@dataclass
class Node:
  # Island Info
  island_lim: int = 0
  island_count: int = 0
  island_dir_count: List[int] = field(default_factory=lambda: [0] * 16)
  # Bridge Info
  bridge_orientation: Orientations = Orientations.NULL
  bridge_amount: int = 0

@dataclass
class NeighbourNode:
  n: Node
  d: Directions

@dataclass
class Move:
  x: int
  y: int
  bridge_amounts: List[int]
  nnodes: List[NeighbourNode]

@dataclass
class State:
  rows: int 
  cols: int
  nodes: List[Node]


def is_island(n):
  return n.island_lim != 0

def get_it_and_orientation(hashi_state, x, y, d):
  it = range(0, 0)
  orientation = Orientations.NULL
  if d == Directions.RIGHT or d == Directions.LEFT:
    orientation = Orientations.HORIZONTAL
    if d == Directions.RIGHT:
      it = range(x + 1, hashi_state.cols)
    else:
      it = range(x - 1, -1, -1)
  elif d == Directions.UP or d == Directions.DOWN:
    orientation = Orientations.VERTICAL
    if d == Directions.UP:
      it = range(y - 1, -1, -1)
    else:
      it = range(y + 1, hashi_state.rows)

  return it, orientation

def can_place_bridge(hashi_state, x, y, d, amount=1):
  n = get_node(hashi_state, x, y)
  if (n.island_lim - n.island_count < amount) or (n.island_dir_count[d.value] + amount) > 3:
    return False

  it, orientation = get_it_and_orientation(hashi_state, x, y, d)

  for i in it:
    n1 = Node()
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, y)
    else:
      n1 = get_node(hashi_state, x, i)
    if is_island(n1):
      if (n1.island_lim - n1.island_count >= amount) and (n1.island_dir_count[~d.value] + amount) <= 3:
        return True
      else:
        return False
    elif n1.bridge_amount > 0 and n1.bridge_orientation != orientation:
      return False

  return False

def remove_bridge(hashi_state, x, y, d):
  place_bridge(hashi_state, x, y, d, True)

def place_bridge(hashi_state, x, y, d, remove=False, amount=1):
  it, orientation = get_it_and_orientation(hashi_state, x, y, d)
  inc = -amount if remove else amount

  n0 = get_node(hashi_state, x, y)
  n1 = Node()
  for i in it:
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, y)
    else:
      n1 = get_node(hashi_state, x, i)
    if is_island(n1):
      break
    else:
      n1.bridge_amount += inc
      assert n1.bridge_amount <= 3, "ok"
      if n1.bridge_amount == 0:
        n1.bridge_orientation = Orientations.NULL
      else:
        n1.bridge_orientation = orientation

  n0.island_count += inc
  n0.island_dir_count[d.value] += inc
  n1.island_count += inc
  n1.island_dir_count[~d.value] += inc


def get_effective_neighbour_nodes(hashi_state, x, y):
  nns = []

  for d in Directions:
    it, orientation = get_it_and_orientation(hashi_state, x, y, d)
    for i in it:
      if orientation == Orientations.HORIZONTAL:
        n = get_node(hashi_state, i, y)
      else:
        n = get_node(hashi_state, x, i)
      if is_island(n) and n.island_count != n.island_lim and n.island_dir_count[~d.value] < 3:
        nn = NeighbourNode(n, d)
        nns.append(nn)
        break
      elif n.bridge_amount > 0 and n.bridge_orientation != orientation:
        break

  return nns


def find_combinations(target_sum, num_elements):
  def generate_combinations(current_combination, remaining_elements):
    if len(current_combination) == num_elements:
      if sum(current_combination) == target_sum:
          combinations.append(tuple(current_combination))
      return

    for num in range(4):
      if num <= remaining_elements:
        generate_combinations(current_combination + [num], remaining_elements - num)

  combinations = []
  generate_combinations([], target_sum)
  return combinations

def gen_moves(hashi_state, x, y):
  n = get_node(hashi_state, x, y)
  nn = get_effective_neighbour_nodes(hashi_state, x, y)
  if len(nn) == 0:
    return []
  target = (n.island_lim - n.island_count)
  moves = []
  for c in find_combinations(target, len(nn)):
    m = Move(x, y, c, nn)
    moves.append(m)

  min_nnode_lim = 10000
  min_nnode_i = 0
  for (i, nnode) in enumerate(nn):
    if nnode.n.island_lim < min_nnode_lim:
      min_nnode_lim = nnode.n.island_lim
      min_nnode_i = i 

  moves.sort(key=lambda move: move.bridge_amounts[min_nnode_i], reverse=True)

  return moves

def move_valid(hashi_state, move):
  for i in range(len(move.bridge_amounts)):
    nn = move.nnodes[i]
    amount = move.bridge_amounts[i]
    if not can_place_bridge(hashi_state, move.x, move.y, nn.d, amount):
      return False
  return True

def apply_move(hashi_state, move):
  for i in range(len(move.bridge_amounts)):
    nn = move.nnodes[i]
    amount = move.bridge_amounts[i]
    place_bridge(hashi_state, move.x, move.y, nn.d, False, amount)

def undo_move(hashi_state, move):
  for i in range(len(move.bridge_amounts)):
    nn = move.nnodes[i]
    amount = move.bridge_amounts[i]
    place_bridge(hashi_state, move.x, move.y, nn.d, True, amount)

def place_definite_bridges(hashi_state):
  x_it = range(hashi_state.cols)
  y_it = range(hashi_state.rows)
  placed_bridges = False
  for y in y_it:
    for x in x_it:
      n = get_node(hashi_state, x, y)
      if not is_island(n) or n.island_count == n.island_lim:
        continue

      nn = get_effective_neighbour_nodes(hashi_state, x, y)

      if len(nn) == 1:
        placed_bridges = True
        for i in range(n.island_lim - n.island_count):
          place_bridge(hashi_state, x, y, nn[0].d)
        continue

      max_bridges_possible = 0
      for neighbour in nn:
        nnode = neighbour.n
        possible = 3 - nnode.island_dir_count[~neighbour.d.value]
        max_bridges_possible += possible 
      if (n.island_lim - n.island_count) == max_bridges_possible:
        placed_bridges = True
        for neighbour in nn:
          for i in range(neighbour.n.island_lim):
            if can_place_bridge(hashi_state, x, y, neighbour.d):
              place_bridge(hashi_state, x, y, neighbour.d)

  return placed_bridges

def solve_hashi(hashi_state):
  placed_bridge = place_definite_bridges(hashi_state)
  while placed_bridge:
    placed_bridge = place_definite_bridges(hashi_state)
  return solve_from_cell(hashi_state, 0, 0)

def solve_from_cell(hashi_state, x, y):
  if x == hashi_state.cols:
    x = 0
    y += 1
    
    if y == hashi_state.rows:
      return True

  n = get_node(hashi_state, x, y)
  if not is_island(n) or n.island_count == n.island_lim:
    return solve_from_cell(hashi_state, x + 1, y)

  possible_moves = gen_moves(hashi_state, x, y)
  for move in possible_moves:
    if move_valid(hashi_state, move):
      apply_move(hashi_state, move)
      if solve_from_cell(hashi_state, x + 1, y):
        return True
      else:
        undo_move(hashi_state, move)

  return False

def get_node(hashi_state, x, y):
  if x < 0 or y < 0 or x >= hashi_state.cols or y >= hashi_state.rows:
    return Node()
  else:
    return hashi_state.nodes[y * hashi_state.cols + x]

def print_hashi_state(hashi_state):
  horizontal_bridge_char = [" ", "-", "=", "E"]
  vertical_bridge_char = [" ", "|", "\"", "#"]
  s = ""
  for y in range(0, hashi_state.rows):
    for x in range(0, hashi_state.cols):
      i = y * hashi_state.cols + x
      n = hashi_state.nodes[i] 

      if is_island(n):
        s += f"{hex(n.island_lim)[2:]}"
      else:
        if n.bridge_orientation == Orientations.HORIZONTAL:
          s += horizontal_bridge_char[n.bridge_amount]
        else:
          s += vertical_bridge_char[n.bridge_amount]
    s += "\n"
  print(s, end="", flush=True)

def parse_hashi_from_stdin():
  nodes = []
  cols = 0
  rows = 0
  for line in sys.stdin:
    cols = len(line) - 1
    for i in range(len(line) - 1):
      n = Node()
      bridge_amount = 0
      try:
        bridge_amount = int(line[i], 16)
      except ValueError:
        pass
      n.island_lim = bridge_amount 
      nodes.append(n)
    rows += 1

  return State(rows, cols, nodes)

def main():
  hashi_state = parse_hashi_from_stdin()
  if solve_hashi(hashi_state):
    print_hashi_state(hashi_state)

if __name__ == "__main__":
  main()
