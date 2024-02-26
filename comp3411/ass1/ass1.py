#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import pathlib
import os
import sys
import subprocess
import logging
import platform
import math

from dataclasses import dataclass
from typing import List
from enum import Enum

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


def clamp(val, limit):
  clamped_val = val

  if val < 0:
    clamped_val = 0
  elif val >= limit:
    clamped_val = limit - 1
  
  return clamped_val

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
  UP = 0b1001
  DOWN = 0b0110
  LEFT = 0b1100
  RIGHT = 0b0011

class Orientations(Enum):
  NULL = 0
  VERTICAL = 1
  HORIZONTAL = 2

@dataclass
class Node:
  # Base Info
  base_lim: int = 0
  base_count: int = 0
  # Bridge Info
  bridge_orientation: Orientations = Orientations.NULL
  bridge_amount: int = 0
  # Location Info
  x: int = 0
  y: int = 0

@dataclass
class State:
  rows: int = 0
  cols: int = 0
  nodes: List[Node]
  required_bridges: int = 0
  num_bridges: int = 0

def parse_hashi_str(hashi_str):
  lines = hashi_str.splitlines()
  cols = len(lines[0])
  rows = len(lines)

  nodes = []
  required_bridges = 0

  for (y, line) in enumerate(lines):
    for i in range(len(line)):
      n = Node()
      bridge_amount = 0
      try:
        bridge_amount = int(line[i], 16)
      except ValueError:
        pass
      n.base_lim = bridge_amount 
      n.x = i
      n.y = y
      nodes.append(n)

      required_bridges += bridge_amount

  s = State(rows, cols, nodes, required_bridges)

  return s

@dataclass
class Move:
  # Node move applied on
  n0_i: int = 0
  # Destination
  n1_i: int = 0
  direction: Directions = Directions.NULL 

def is_base(n):
  return n.base_lim != 0

def get_next_base_i(hashi_state, i):
  node_i = i + 1 if i > 0 else i
  n = hashi_state.nodes[node_i]
  while !is_base(n):
    node_i += 1
    n = hashi_state.nodes[node_i]
  return node_i

def get_it_and_orientation(hashi_state, n, d):
  it = range(0, 0)
  orientation = Orientations.NULL
  if d == Direction.RIGHT || d == Direction.LEFT:
    orientation = Orientations.HORIZONTAL
    if d == Direction.RIGHT:
      it = range(n.x + 1, hashi_state.cols)
    else:
      it = range(n.x - 1, -1, -1)
  elif d == Direction.UP || d == Direction.DOWN:
    orientation = Orientations.VERTICAL
    if d == Directions.UP:
      it = range(n.y - 1, -1, -1)
    else:
      it = range(n.y + 1, hashi_state.rows)

  return it, orientation

def gen_move(hashi_state, n, d):
  it, orientation = get_it_and_orientation(hashi_state, n, d)

  move = Move()
  for i in it:
    n1 = Node()
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, n.y)
    else:
      n1 = get_node(hashi_state, n.x, i)
    if !is_base(n1) && n1.bridge_amount > 0 && n1.bridge_orientation != orientation:
      break
    elif n1.base_count < n1.base_lim:
      move = Move(n0_i, n1_i, d)
      break

  return move


def push_possible_moves(hashi_state, n, next_moves):
  num_moves = 0

  for d in Directions:
    move = gen_move(hashi_state, n, d)
    if move.direction != Directions.NULL:
      next_moves.append(move)
      num_moves += 1
  return num_moves

# IMPORTANT(Ryan): All moves are checked for validity prior
def apply_move(hashi_state, move, move_history):
  place_bridge(hashi_state, move.n0, move.n1, move.direction, False)
  move_history.append(move)

def undo_move(hashi_state, move_history):
  move = move_history.pop()
  place_bridge(hashi_state, move.n0, move.n1, move.direction, True)
  return move.n0

def solve_hashi(hashi_state):
  next_moves = [] 
  move_history = []

  cur_node = hashi_state.nodes[0]

  solved = False

  undo_state = False
  while !node_equal(cur_node, hashi_state.nodes[-1]):
    # Check if need to undo
    if undo_state:
      # If next move is applied on a different node, undo again
      if !node_equal(next_moves[-1].n0, cur_node): 
        cur_node = undo_move(hashi_state, move_history)
      else:
        move = next_moves.pop()
        apply_move(hashi_state, move, move_history)
        undo_state = False
      continue
    # Check if base needs more bridges
    elif cur_node.base_count < cur_node.base_lim:
      move_amount = push_possible_moves(hashi_state, cur_node, next_moves)
      if move_amount == 0:
        undo_state = True
        cur_node = undo_move(hashi_state, move_history)
        continue
      else:
        move = next_moves.pop()
        apply_move(hashi_state, move, move_history)
    else:
      cur_node_i = cur_node.y * hashi_state.cols + cur_node.x
      cur_node = hashi_state.nodes[cur_node_i + 1]

    # Check if solved
    if hashi_state.num_bridges == hashi_state.required_bridges:
      solved = True
      break

  return solved


def get_node(hashi_state, x, y):
  if x < 0 || y < 0 || x >= hashi_state.rows || y >= hashi_state.cols:
    return Node()
  else:
    return hashi_state.nodes[y * hashi_state.rows + x]

def node_equal(n0, n1):
  return n0.x == n1.x && n0.y == n1.y

def place_bridge(hashi_state, n0, n1, d, remove):
  it, orientation = get_it_and_orientation(hashi_state, n0, d)
  inc = -1 if remove else 1

  for i in it:
    n = Node()
    if orientation == Orientations.HORIZONTAL:
      n = get_node(hashi_state, i, n.y)
    else:
      n = get_node(hashi_state, n.x, i)
    if node_equal(n, n1):
      break
    else:
      n.bridge_amount += inc
      if n.bridge_amount == 0:
        n.bridge_orientation = orientations.NULL
      else:
        n.bridge_orientation = orientation

  n0.base_count += inc
  n1.base_count += inc
  hashi_state.num_bridges += inc

def main():
  hashi_str = read_entire_file("hashi.puzzle")
  hashi_state = parse_hashi_str(hashi_str)
  solve_hashi(hashi_state)

if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
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

  trace(f"python: {platform.python_version()}")

  main()

