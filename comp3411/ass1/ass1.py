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

  for line in lines:
    for i in range(len(line)):
      n = Node()
      bridge_amount = 0
      try:
        bridge_amount = int(line[i], 16)
      except ValueError:
        pass
      n.base_lim = bridge_amount 
      nodes.append(n)

      required_bridges += bridge_amount

  s = State(rows, cols, nodes, required_bridges)

  return s


@dataclass
class Move:
  n1: Node = Node()
  direction: Directions = Directions.NULL 

def is_base(n):
  return n.base_lim != 0

def get_next_base(hashi_state, i):
  node_i = i + 1 if i > 0 else i
  n = hashi_state.nodes[node_i]
  while !is_base(n):
    node_i += 1
    n = hashi_state.nodes[node_i]
  return n, node_i

def solve_hashi(hashi_state):
  next_moves = [] 
  move_history = []

  cur_node, node_i = get_next_base(hashi_state, 0)

  undo_state = False
  while node_i < len(hash_state.nodes):
    # Check if solved
    if hashi_state.num_bridges == hashi_state.required_bridges:
      break
    # Check if base needs more bridges
    if cur_node.base_count < cur_node.base_lim:
      if undo_state:
        undo_move(hashi_state, move_history)
      else:
        move_amount = push_possible_moves(hashi_state, cur_node, next_moves)
        if move_amount == 0:
          undo_state = True
          continue
      assert len(next_moves) > 0, "No solution"
      move = next_moves.pop()
      apply_move(hashi_state, move, move_history)
      undo_state = False
    else:
      cur_node, node_i = get_next_base(hashi_state, node_i)


def get_node(hashi_state, x, y):
  if x < 0 || y < 0 || x >= hashi_state.rows || y >= hashi_state.cols:
    return Node()
  else:
    return hashi_state.nodes[y * hashi_state.rows + x]

def get_accessible_nnode(hashi_state, x, y, d):
  if d == Direction.RIGHT || d == Direction.LEFT:
    if d == Direction.RIGHT:
      start = x + 1
      end = hashi_state.cols 
    else:
      start = x - 1
      end = -1
    for i in range(start, end):
      n = get_node(hashi_state, i, y)
      if n.amount > 0 && n.orientation != Orientation.HORIZONTAL:
        return Node(), 0, 0
      if n.lim != 0:
        return n, i, y
  elif d == Direction.UP || d == Directions.DOWN:
    if d == Directions.UP:
      start = y - 1
      end = -1
    else:
      start = y + 1
      end = hashi_state.rows
    for i in range(start, y1):
      n = get_node(hashi_state, x, i)
      if n.amount > 0 && n.orientation != Orientation.VERTICAL:
        return Node(), 0, 0
      if n.lim != 0:
        return n, x, i

  return Node(), 0, 0

def place_bridge(hashi_state, x, y, d):
  n = get_node(hashi_state, x, y)
  nn, x1, y1 = get_accessible_nnode(hashi_state, x, y, d) 

  if n.count < n.lim && nn.count < nn.lim:
    n.count += 1
    nn.count += 1

    if d == Direction.RIGHT || d == Direction.LEFT:
      if d == Direction.RIGHT:
        start = x + 1
      else:
        start = x - 1
      for i in range(start, x1):
        n = get_node(hashi_state, i, y)
        n.amount += 1
        n.orientation = Orientations.HORIZONTAL
    elif d == Direction.UP || d == Directions.DOWN:
      if d == Directions.UP:
        start = y - 1
      else:
        start = y + 1
      for i in range(start, y1):
        n = get_node(hashi_state, x, i)
        n.amount += 1
        n.orientation = Orientations.VERTICAL

     return True

  return False

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

