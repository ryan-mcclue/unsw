#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import sys
import socket
import random

from dataclasses import dataclass, field
from typing import List
from enum import Enum

import sys

global_num_cells = 9 # width
global_num_boards = 9 # height
global_grid = [0] * global_num_cells * global_num_boards
global_next_board_num = 0

class Mark(Enum):
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

def grid_coord(board_num, cell_num):
  return (board_num - 1) * global_num_cells + (cell_num - 1)

def place_mark(board_num, cell_num, mark):
  global global_next_board_num
  global global_grid

  coord = grid_coord(board_num, cell_num)

  global_grid[coord] = mark
  
  global_next_board_num = cell_num

def make_move():
  global global_grid
  global global_next_board_num

  n = random.randint(1, 9)
  coord = grid_coord(global_next_board_num, n)
  while global_grid[coord] != Mark.EMPTY.value:
    n = random.randint(1, 9)
    coord = grid_coord(global_next_board_num, n)

  place_mark(global_next_board_num, n, Mark.PLAYER)

  return n

def parse_cmd(cmd):
  if "(" in cmd:
    command, args = cmd.split("(")
    args = args.split(")")[0]
    args = args.split(",")
  else:
    command, args = cmd, []

  print(f"{command}, {args}")

  if command == "init":
    return 0
  elif command == "second_move":
    # going second, i.e. 'o'
    opponent_board_num = int(args[0])
    opponent_cell_num = int(args[1])

    # place server generated random move for opponent
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "third_move":
    # going first, i.e. 'x'
    our_random_board_num = int(args[0])
    our_random_cell_num = int(args[1])
    opponent_board_num = our_random_cell_num
    opponent_cell_num = int(args[2])

    # place our server generated random move
    place_mark(our_random_board_num, our_random_cell_num, Mark.PLAYER)
    # place opponents move
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "next_move":
    opponent_board_num = global_next_board_num
    opponent_cell_num = int(args[0])

    # place opponent move
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "win":
    print("Yay!! We win!! :)")
    return -1
  elif command == "loss":
    print("We lost :(")
    return -1
  elif command == "draw":
    print("Draw")
    # TODO: how to handle this?
    return -1

  return 0

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

  s.connect(('localhost', port))
  while True:
    text = s.recv(1024).decode()
    if not text:
      continue
    for cmd in text.split("\n"):
      response = parse_cmd(cmd)
      if response == -1:
        s.close()
        return
      elif response > 0:
        s.sendall((str(response) + "\n").encode())


if __name__ == "__main__":
  main()
