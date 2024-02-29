#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

# Briefly describe how your program works, including any algorithms and data
# structures employed, and explain any design decisions you made along the
# way.

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
#     By combining information, can have one node type to simplify map representation
#     Storage for an island node:
#       - Number of connected bridges
#       - Number of the currently connected bridges
#       - Number of bridges connected in a particular direction
#     Storage for a bridge node:
#       - Orientation of bridge
#       - How many bridges
#   State class:
#     Encodes map. Stores number of rows, columns and a node array of row*columns size.
# 
# Algorithms:
#   hashi_solve() employs a backtracking algorithm. 
#   It is a recursive DFS implementation.
#   Reasons DFS was chosen:
#     - Simpler than an informed search
#     - Knew no cycles, so would not get stuck
#     - There is no optimal solution, so sub-optimal limitations not a concern.
#       Get added bonus of linear space complexity over BFS.
#   Each island is iterated over until each has required number of connected bridges.
#   For each island, all possible directions for adding a bridge are explored.
#   If can place a bridge in this direction, recurse on it, i.e. explore this option.
#   If exploring this option does not yield solution, remove bridge.
#   If reach one past the dimensions of the map, know have solved, so return.     

import pathlib
import os
import sys
import subprocess
import logging
import platform
import math
import copy

from dataclasses import dataclass, field
from typing import List
from enum import Enum

def debugger():
  return sys.gettrace() is not None

global global_logger

def fatal_error(msg):
  global_logger.critical(msg)
  breakpoint()
  sys.exit()

def warn(msg):
  global_logger.warning(msg)
  # NOTE(Ryan): Disable by passing -O to interpreter
  if __debug__:
    breakpoint()
    sys.exit()

def trace(msg):
  if __debug__:
    global_logger.debug(msg)

def read_entire_file(name):
  res = ""
  try:
    f = open(name, 'r')
    res = f.read()
    f.close()
  except Exception as e:
    warn(f"Unable to read file {name}.\n{e}")
  return res

class Directions(Enum):
  NULL = 0
  UP = 0b01
  DOWN = 0b10
  LEFT = 0b1100
  RIGHT = 0b0011

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

  def __str__(self):
    return f"({self.x},{self.y}:{self.island_count}/{self.island_lim})"

@dataclass
class State:
  rows: int 
  cols: int
  nodes: List[Node]

  def __str__(self):
    return f"({self.n0}->{self.n1})"

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

def solve_hashi(hashi_state):
  return solve_from_cell(hashi_state, 0, 0)

deepest_state = None
furthest_x = -1
furthest_y = -1
furthest = -1

def solve_with_bp(hashi_state, x, y):
  if x == hashi_state.cols:
    x = 0
    y += 1
    
    if y == hashi_state.rows:
      return True

  global furthest_x
  global furthest_y
  if x == furthest_x and y == furthest_y:
    breakpoint()

  n = get_node(hashi_state, x, y)
  if not is_island(n) or n.island_count == n.island_lim:
    return solve_with_bp(hashi_state, x + 1, y)

  for d in Directions:
    if can_place_bridge(hashi_state, x, y, d):
      place_bridge(hashi_state, x, y, d)
      if solve_with_bp(hashi_state, x, y):
        return True
      else:
        remove_bridge(hashi_state, x, y, d)

  return False


def solve_from_cell(hashi_state, x, y):
  # goal state is when solved last item
  if x == hashi_state.cols:
    x = 0
    y += 1
    
    if y == hashi_state.rows:
      return True

  # NOTE(Ryan): For debugging
  global deepest_state
  global furthest_x
  global furthest_y
  global furthest
  coord = y * hashi_state.cols + x
  if coord > furthest:
    furthest = coord
    furthest_x = x
    furthest_y = y
    deepest_state = copy.deepcopy(hashi_state)

  n = get_node(hashi_state, x, y)
  if not is_island(n) or n.island_count == n.island_lim:
    return solve_from_cell(hashi_state, x + 1, y)

  # this for loop is for exploration
  for d in Directions:
    if can_place_bridge(hashi_state, x, y, d):
      place_bridge(hashi_state, x, y, d)
      if solve_from_cell(hashi_state, x, y):
        return True
      else:
        # remove decision if coming up
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
  print(s, end="")

def parse_hashi_from_file():
  hashi_str = read_entire_file("hashi.puzzle")
  lines = hashi_str.splitlines()
  cols = len(lines[0])
  rows = len(lines)

  nodes = []

  for line in lines:
    for i in range(len(line)):
      n = Node()
      bridge_amount = 0
      try:
        bridge_amount = int(line[i], 16)
      except ValueError:
        pass
      n.island_lim = bridge_amount 
      nodes.append(n)

  return State(rows, cols, nodes)

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
  hashi_state = None
  hashi_state_copy = None
  if debugger():
    hashi_state = parse_hashi_from_file()
    hashi_state_copy = copy.deepcopy(hashi_state)
  else:
    hashi_state = parse_hashi_from_stdin()

  solved = solve_hashi(hashi_state)
  if solved:
    print_hashi_state(hashi_state)
  else:
    solve_with_bp(hashi_state_copy, 0, 0)
    print_hashi_state(deepest_state)


if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if not debugger():
    os.environ["PYTHONBREAKPOINT"] = "0"
  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  global_logger = logging.getLogger(__name__)
  global_logger.setLevel(logging.DEBUG)
  global_logger_handler = logging.StreamHandler()
  global_logger_handler.setLevel(logging.DEBUG)
  global_logger_formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
  global_logger_handler.setFormatter(global_logger_formatter)
  global_logger.addHandler(global_logger_handler)

  main()
