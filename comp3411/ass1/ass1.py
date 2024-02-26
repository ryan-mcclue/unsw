#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import pathlib
import os
import sys
import subprocess
import logging
import platform
import math

from dataclasses import dataclass, field
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
  # Base Info
  base_lim: int = 0
  base_count: int = 0
  base_dir_count: List[int] = field(default_factory=lambda: [0] * 16)
  # Bridge Info
  bridge_orientation: Orientations = Orientations.NULL
  bridge_amount: int = 0
  # Location Info
  x: int = 0
  y: int = 0

  def __str__(self):
    return f"({self.x},{self.y}:{self.base_count}/{self.base_lim})"

@dataclass
class State:
  rows: int 
  cols: int
  num_bridges: int
  nodes: List[Node]


@dataclass
class Move:
  # Node move applied on
  n0: Node = Node()
  # Destination
  n1: Node = Node()
  direction: Directions = Directions.NULL 

  def __str__(self):
    return f"({self.n0}->{self.n1})"

def is_base(n):
  return n.base_lim != 0

def get_it_and_orientation(hashi_state, n, d):
  it = range(0, 0)
  orientation = Orientations.NULL
  if d == Directions.RIGHT or d == Directions.LEFT:
    orientation = Orientations.HORIZONTAL
    if d == Directions.RIGHT:
      it = range(n.x + 1, hashi_state.cols)
    else:
      it = range(n.x - 1, -1, -1)
  elif d == Directions.UP or d == Directions.DOWN:
    orientation = Orientations.VERTICAL
    if d == Directions.UP:
      it = range(n.y - 1, -1, -1)
    else:
      it = range(n.y + 1, hashi_state.rows)

  return it, orientation

def is_move_valid(hashi_state, move):
  n0 = move.n0
  n1 = move.n1
  d = move.direction

  if n0.base_count < n0.base_lim and n0.base_dir_count[d.value] < 3 and \
     n1.base_count < n1.base_lim and n1.base_dir_count[~d.value] < 3:
    return True
  else:
    return False

def gen_move(hashi_state, n, d):
  it, orientation = get_it_and_orientation(hashi_state, n, d)

  move = Move()
  if n.base_count >= n.base_lim or n.base_dir_count[d.value] >= 3:
    return move

  for i in it:
    n1 = Node()
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, n.y)
    else:
      n1 = get_node(hashi_state, n.x, i)
    if is_base(n1):
      if n1.base_count < n1.base_lim and n1.base_dir_count[~d.value] < 3:
        move = Move(n, n1, d)
      break
    elif n1.bridge_amount > 0 and n1.bridge_orientation != orientation:
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
  #print_hashi_state(hashi_state)

def undo_move(hashi_state, move_history):
  move = move_history.pop()
  #print(f"undoing ({move.n0.x},{move.n0.y}),({move.n1.x},{move.n1.y}){move.direction}")
  place_bridge(hashi_state, move.n0, move.n1, move.direction, True)
  #print_hashi_state(hashi_state)
  return move.n0

def solve_hashi(hashi_state):
  next_moves = [] 
  move_history = []

  cur_node = hashi_state.nodes[0]

  solved = False
  final_node = hashi_state.nodes[-1]

  undo_state = False
  while True: 
    #print(f"({cur_node.x},{cur_node.y}:{final_node.x},{final_node.y})")
    # Check if need to undo
    if undo_state:
      move = Move()
      # check all moves for this node to see if require another undo
      while node_equal(next_moves[-1].n0, cur_node):
        move = next_moves.pop()
        if is_move_valid(hashi_state, move):
          break
        else:
          if len(next_moves) == 0:
            move_amount = push_possible_moves(hashi_state, cur_node, next_moves)
            if move_amount == 0:
             undo_move(hashi_state, move_history)
             cur_node = move_history[-1].n0

      if not is_move_valid(hashi_state, move):
        undo_move(hashi_state, move_history)
        cur_node = move_history[-1].n0
      else:
        apply_move(hashi_state, move, move_history)
        undo_state = False
      continue
    # Check if base needs more bridges
    elif cur_node.base_count < cur_node.base_lim:
      move_amount = push_possible_moves(hashi_state, cur_node, next_moves)
      if move_amount == 0:
        undo_state = True
        undo_move(hashi_state, move_history)
        cur_node = move_history[-1].n0
        continue
      else:
        move = next_moves.pop()
        apply_move(hashi_state, move, move_history)
    else:
      if node_equal(cur_node, final_node):
        if is_base(cur_node) and cur_node.base_count == cur_node.base_lim:
          solved = True
          break
        else:
          break
      else:
        cur_node_i = cur_node.y * hashi_state.cols + cur_node.x
        cur_node = hashi_state.nodes[cur_node_i + 1]

  return solved


def get_node(hashi_state, x, y):
  if x < 0 or y < 0 or x >= hashi_state.rows or y >= hashi_state.cols:
    return Node()
  else:
    return hashi_state.nodes[y * hashi_state.cols + x]

def node_equal(n0, n1):
  return n0.x == n1.x and n0.y == n1.y

def place_bridge(hashi_state, n0, n1, d, remove):
  it, orientation = get_it_and_orientation(hashi_state, n0, d)
  inc = -1 if remove else 1

  #if remove:
  #  print(f"removing {n0.base_lim}:{n1.base_lim}:{d}")
  #else:
  #  print(f"adding {n0.base_lim}:{n1.base_lim}:{d}")

  for i in it:
    n = Node()
    if orientation == Orientations.HORIZONTAL:
      n = get_node(hashi_state, i, n0.y)
    else:
      n = get_node(hashi_state, n0.x, i)
    if node_equal(n, n1):
      break
    else:
      assert not is_base(n), f"{n0.base_lim}:{n1.base_lim} adding bridge on {n.x},{n.y}"
      n.bridge_amount += inc
      assert n.bridge_amount <= 3, "less"
      if n.bridge_amount == 0:
        n.bridge_orientation = Orientations.NULL
      else:
        n.bridge_orientation = orientation

  n0.base_count += inc
  n0.base_dir_count[d.value] += inc
  n1.base_count += inc
  n1.base_dir_count[~d.value] += inc
  hashi_state.num_bridges += inc

def print_hashi_state(hashi_state):
  horizontal_bridge_char = [".", "-", "=", "E", "X"]
  vertical_bridge_char = [".", "|", "\"", "#", "X"]
  s = ""
  for y in range(0, hashi_state.rows):
    for x in range(0, hashi_state.cols):
      i = y * hashi_state.cols + x
      n = hashi_state.nodes[i] 

      if is_base(n):
        s += f"{hex(n.base_lim)[2:]}"
      else:
        if n.bridge_orientation == Orientations.HORIZONTAL:
          s += horizontal_bridge_char[n.bridge_amount]
        else:
          s += vertical_bridge_char[n.bridge_amount]
    s += "\n"
  print(s, end="\n")

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

  s = State(rows, cols, 0, nodes)

  return s

def main():
  hashi_str = read_entire_file("hashi.puzzle")
  hashi_state = parse_hashi_str(hashi_str)
  solve_hashi(hashi_state)
  print_hashi_state(hashi_state)


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

