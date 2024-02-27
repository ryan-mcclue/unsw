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

  def __str__(self):
    return f"({self.x},{self.y}:{self.base_count}/{self.base_lim})"

@dataclass
class State:
  rows: int 
  cols: int
  num_bridges: int
  nodes: List[Node]

  def __str__(self):
    return f"({self.n0}->{self.n1})"

def is_base(n):
  return n.base_lim != 0

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
  if n.base_count >= n.base_lim or n.base_dir_count[d.value] >= 3:
    return False

  it, orientation = get_it_and_orientation(hashi_state, x, y, d)

  for i in it:
    n1 = Node()
    if orientation == Orientations.HORIZONTAL:
      n1 = get_node(hashi_state, i, y)
    else:
      n1 = get_node(hashi_state, x, i)
    if is_base(n1):
      if n1.base_count < n1.base_lim and n1.base_dir_count[~d.value] < 3:
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
    if is_base(n1):
      break
    else:
      n1.bridge_amount += inc
      if n1.bridge_amount == 0:
        n1.bridge_orientation = Orientations.NULL
      else:
        n1.bridge_orientation = orientation

  n0.base_count += inc
  n0.base_dir_count[d.value] += inc
  n1.base_count += inc
  n1.base_dir_count[~d.value] += inc
  hashi_state.num_bridges += inc


# 1. Reduce to solving for smallest element, i.e. a base
# 2. Iterate over all possible choices for element:
#    If choice valid, recurse on moving along, else undo
# 3. If x overflow, update to new location
#    If y overflow, know have reached goal state

def solve_hashi(hashi_state):
  return solve_from_cell(hashi_state, 0, 0)

def solve_from_cell(hashi_state, x, y):
  # goal state is when solved last item
  if x == hashi_state.cols:
    x = 0
    y += 1
    if y == hashi_state.rows:
      return True

  n = get_node(hashi_state, x, y)
  if not is_base(n):
    return solve_from_cell(hashi_state, x + 1, y)
  elif n.base_count == n.base_lim:
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
  if x < 0 or y < 0 or x >= hashi_state.rows or y >= hashi_state.cols:
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

      if is_base(n):
        s += f"{hex(n.base_lim)[2:]}"
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

  s = State(rows, cols, 0, nodes)

  return s

def parse_hashi_from_stdin():
  nodes = []
  cols = 0
  rows = 0
  for line in sys.stdin:
    cols = len(line) - 1
    for i in range(len(line)):
      n = Node()
      bridge_amount = 0
      try:
        bridge_amount = int(line[i], 16)
      except ValueError:
        pass
      n.base_lim = bridge_amount 
      nodes.append(n)
    rows += 1

  return State(rows, cols, 0, nodes)

def main():
  #hashi_state = parse_hashi_from_stdin()
  hashi_state = parse_hashi_from_file()

  if solve_hashi(hashi_state):
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

  main()
