#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import sys
import socket
import random

from dataclasses import dataclass, field
from typing import List
from enum import Enum

import sys

class Mark(Enum):
  PLAYER = 0
  OPPONENT = 1
  EMPTY = 2

global_num_cells = 9 # width
global_num_boards = 9 # height
global_grid = [Mark.EMPTY.value] * global_num_cells * global_num_boards
global_next_board_num = 0

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

def has_mark_won(mark):
  global global_grid
  global global_next_board_num

  active_board_coord = grid_coord(global_next_board_num, 0)
  active_board = global_grid[active_board_coord]

  # 0 1 2
  # 3 4 5
  # 6 7 8
  left_col = (active_board[0] == mark and active_board[3] == mark and active_board[6] == mark)
  middle_col = (active_board[1] == mark and active_board[4] == mark and active_board[7] == mark)
  right_col = (active_board[2] == mark and active_board[5] == mark and active_board[8] == mark)
  top_row = (active_board[0] == mark and active_board[1] == mark and active_board[2] == mark)
  middle_row = (active_board[3] == mark and active_board[4] == mark and active_board[5] == mark)
  bottom_row = (active_board[6] == mark and active_board[7] == mark and active_board[8] == mark)
  left_diag = (active_board[0] == mark and active_board[4] == mark and active_board[8] == mark)
  right_diag = (active_board[6] == mark and active_board[4] == mark and active_board[2] == mark)

  return (left_col or middle_col or right_col or top_row or middle_row or bottom_row or left_diag or right_diag)

def minimax(position, depth, maximising_mark):
  if depth == 0 or has_mark_won(maximising_mark.value ^ 1):
    return -1000 + m?; # static evaluation

  if maximising_mark == Mark.PLAYER:
    max_val = -100000
    for move in possible_moves at position:
      val = minimax(position, depth-1, maximising_mark.value ^ 1)
      max_val = max(max_val, val)
    return max_val
  else:
    min_val = 100000
    # TODO: if no legal moves, draw and return 0;
    for move in possible_moves at position:
      make_move(move)
      val = minimax(position, depth-1, maximising_mark.value ^ 1)
      min_val = min(min_val, val)
      undo_move(move)
    return min_val

minimax(board, 50, Mark.PLAYER.value)


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
    # TODO: necessary to handle other commands not explicitly listed in agent.py?
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
