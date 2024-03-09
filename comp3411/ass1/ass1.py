#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

############################################################
# DESCRIPTION
############################################################

# Data Structures:
#   Orientations enum:
#     Provides a readable encoding of a bridge's orientation on the map.
#     NULL indicates no bridge is present.
#   Directions enum:
#     Encodes a connected bridge's direction from the perspective of an island.
#     Opposite directions are encoded as the bitwise and of each other.
#     This allows a bridge's direction to be inverted from the perspective of the destination island.
#   Node class:
#     Encodes a location on the map.
#     Can either be an island or a possible bridge location.
#     They can be told apart as a bridge will have 0 for number of required bridges.
#     By combining information, can have one node type to simplify map representation.
#     Fields for an island node:
#       - Number of connected bridges
#       - Number of the currently connected bridges
#       - Number of bridges connected in a particular direction
#     Fields for a bridge node:
#       - Orientation of bridge
#       - How many bridges currently containing
#   State class:
#     Encodes map. Stores number of rows, columns and a node array of row*columns size.
# 
# Program:
#   The map is read line by line from stdin. 
#   Each character of line is converted to a node thate goes into state object.
#   hashi_solve() takes this state and employs a backtracking algorithm.
#   It is a recursive DFS implementation.
#   Reasons DFS was chosen:
#     - Simpler than an informed search
#     - Knew no cycles, so would not get stuck
#     - There is no optimal solution, so sub-optimal limitations not a concern.
#       Get added bonus of linear space complexity over BFS.
#   Each island is iterated over until each has required number of connected bridges.
#   For each island, all possible directions for adding a bridge are potentially explored.
#   For an island, if can place a bridge in a particular direction, recurse on it, i.e. explore this option.
#   If exploring this option does not yield solution, remove bridge.
#   Base cases:
#     - Recieve coordinates one past the dimensions of the map, know have solved, return true.
#     - No bridges in any direction can be added to the island, return false.
#   The state object is finally printed, representing a solution.

import sys

import time
import os
import signal
import threading

import copy
from collections import deque

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

def can_place_bridge(hashi_state, x, y, d):
  n = get_node(hashi_state, x, y)
  if n.island_count >= n.island_lim or n.island_dir_count[d.value] >= 3:
    return False

  it, orientation = get_it_and_orientation(hashi_state, x, y, d)

  for i in it:
    n1 = Node()
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, y)
    else:
      n1 = get_node(hashi_state, x, i)
    if is_island(n1):
      if n1.island_count < n1.island_lim and n1.island_dir_count[~d.value] < 3:
        return True
      else:
        return False
    elif n1.bridge_amount > 0 and n1.bridge_orientation != orientation:
      return False

  return False

def remove_bridge(hashi_state, x, y, d):
  place_bridge(hashi_state, x, y, d, True)

def place_bridge(hashi_state, x, y, d, remove=False):
  it, orientation = get_it_and_orientation(hashi_state, x, y, d)
  inc = -1 if remove else 1

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
      if n1.bridge_amount == 0:
        n1.bridge_orientation = Orientations.NULL
      else:
        n1.bridge_orientation = orientation

  n0.island_count += inc
  n0.island_dir_count[d.value] += inc
  n1.island_count += inc
  n1.island_dir_count[~d.value] += inc

@dataclass
class NeighbourNode:
  n: Node = Node()
  d: Directions = Directions.NULL

def get_neighbour_nodes(hashi_state, x, y):
  nns = []

  for d in Directions:
    it, orientation = get_it_and_orientation(hashi_state, x, y, d)
    for i in it:
      if orientation == Orientations.HORIZONTAL:
        n = get_node(hashi_state, i, y)
      else:
        n = get_node(hashi_state, x, i)
      if is_island(n):
        nn = NeighbourNode(n, d)
        nns.append(nn)
        break

  return nns

def place_definite_bridges(hashi_state):
  x_it = range(hashi_state.cols)
  y_it = range(hashi_state.rows)
  for y in y_it:
    for x in x_it:
      n = get_node(hashi_state, x, y)
      if not is_island(n):
        continue

      nn = get_neighbour_nodes(hashi_state, x, y)

      if len(nn) == 1:
        # NOTE(Ryan): Ensure not doubling up if other 1 to 1
        if can_place_bridge(hashi_state, x, y, nn[0].d):
          for i in range(n.island_lim):
            place_bridge(hashi_state, x, y, nn[0].d)
        continue

      max_neighbours = (n.island_lim == 12) or \
                       ((n.island_lim == 9) and len(nn) == 3) or \
                       ((n.island_lim == 6) and len(nn) == 2)
      if max_neighbours:
        for neighbour in nn:
          if can_place_bridge(hashi_state, x, y, neighbour.d):
            place_bridge(hashi_state, x, y, neighbour.d)
          if can_place_bridge(hashi_state, x, y, neighbour.d):
            place_bridge(hashi_state, x, y, neighbour.d)
          if can_place_bridge(hashi_state, x, y, neighbour.d):
            place_bridge(hashi_state, x, y, neighbour.d)
        continue

      max_bridges_possible = 0
      for neighbour in nn:
        if nn.n.island_lim <= 3:
          max_bridges_possible += nn.n.island_lim
        else:
          max_bridges_possible += 3
      if max_bridges_possible == n.island_lim:
        for neighbour in nn:
          if can_place_bridge(hashi_state, x, y, neighbour.d):
            place_bridge(hashi_state, x, y, neighbour.d)



  # now, see if (lim - bridges) = sum of neighbours 

def solve_hashi(hashi_state):
  print_hashi_state(hashi_state)
  print("")
  place_definite_bridges(hashi_state)
  print_hashi_state(hashi_state)
  print("")
  #print_hashi_state(hashi_state)
  #return True
  ## perhaps go through and add values we know must exist
  return solve_from_cell(hashi_state, 0, 0, 0)

max_depth = -1

# TODO(Ryan): 40x40 in under 2 minutes
def solve_from_cell(hashi_state, x, y, depth):
  global max_depth
  if depth > max_depth:
    max_depth = depth

  if x == hashi_state.cols:
    x = 0
    y += 1
    
    if y == hashi_state.rows:
      return True

  n = get_node(hashi_state, x, y)
  if not is_island(n) or n.island_count == n.island_lim:
    return solve_from_cell(hashi_state, x + 1, y, depth + 1)

  # go to smaller island degree first as most restrictive
  # neighbour_nodes = get_neighbour_nodes(hashi_state, x, y)
  # neighbour_nodes.sort(key=lambda nn: nn.n.island_lim) 

  # for nn in neighbour_nodes:
  #   if can_place_bridge(hashi_state, x, y, nn.d):
  #     place_bridge(hashi_state, x, y, nn.d)
  #     if solve_from_cell(hashi_state, x, y, depth + 1):
  #       return True
  #     else:
  #       remove_bridge(hashi_state, x, y, nn.d)

  for d in Directions:
    if can_place_bridge(hashi_state, x, y, d):
      place_bridge(hashi_state, x, y, d)
      if solve_from_cell(hashi_state, x, y, depth + 1):
        return True
      else:
        remove_bridge(hashi_state, x, y, d)

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
  # online tests may be sensitive to newline at end

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

def print_max_depth():
  # not depth a concern, rather going down unecessary branches
  global max_depth
  time.sleep(60)
  print(f"EXPIRED: max depth {max_depth}", flush=True)
  exit_all_threads()

def exit_all_threads():
  os._exit(1)

def main():
  hashi_state = parse_hashi_from_stdin()

  # watchdog_thread = threading.Thread(target=print_max_depth)
  # watchdog_thread.start()

  if solve_hashi(hashi_state):
    #print_hashi_state(hashi_state)
    print(f"max depth: {max_depth}", flush=True)
    exit_all_threads()

if __name__ == "__main__":
  main()
