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
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

class Score(Enum):
  END = 100000
  DRAW = 0
  CENTRE = 5
  CORNER = 2
  POSSIBLE_END = 100
  BOARD_COUNT = 1

  MAX_SCORE = 10000000
  MIN_SCORE = -MAX_SCORE

@dataclass
class Move:
  board_num: int = 0
  cell_num: int = 0
  score: int = 0

global_num_cells = 9 # width
global_num_boards = 9 # height
global_grid = [Mark.EMPTY] * global_num_cells * global_num_boards
global_next_board_num = 0

def grid_coord(board_num, cell_num):
  global global_num_cells
  return (board_num - 1) * global_num_cells + (cell_num - 1)

def place_mark(board_num, cell_num, mark):
  global global_next_board_num
  global global_grid

  coord = grid_coord(board_num, cell_num)

  global_grid[coord] = mark
  
  global_next_board_num = cell_num

# def make_move():
#   global global_grid
#   global global_next_board_num
# 
#   n = random.randint(1, 9)
#   coord = grid_coord(global_next_board_num, n)
#   while global_grid[coord] != Mark.EMPTY.value:
#     n = random.randint(1, 9)
#     coord = grid_coord(global_next_board_num, n)
# 
#   place_mark(global_next_board_num, n, Mark.PLAYER)
# 
#   return n

def have_won(grid, cur_board_num, are_max):
  mark = Mark.PLAYER if are_max else Mark.OPPONENT

  active_board_coord = grid_coord(cur_board_num, 1)
  active_board = grid[active_board_coord:active_board_coord+9]

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

def board_score(board, are_max, is_next):
  score = 0
  
  score_mul = 1 if are_max else -1
  mark = Mark.PLAYER if are_max else Mark.OPPONENT

  # centre control
  if board[4] == mark:
    score += (score_mul * Score.CENTRE.value)

  # corner control
  for i in [0, 2, 6, 8]:
    if board[i] == mark:
      score += (score_mul * Score.CORNER.value)

  # if looking at next move, then these give ending moves
  possible_end_score = Score.END.value if is_next else Score.POSSIBLE_END.value

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # possible row
  i=0
  j=1
  k=2
  if board[i] == board[j] and board[i] == mark and board[k] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[k] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[k] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  i+=3
  j+=3
  k+=3
  if board[i] == board[j] and board[i] == mark and board[k] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[k] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[k] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  i+=3
  j+=3
  k+=3
  if board[i] == board[j] and board[i] == mark and board[k] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[k] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[k] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)


  # 0 1 2
  # 3 4 5
  # 6 7 8
  # possible col
  i=0
  j=3
  k=6
  if board[i] == board[6] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[j] and board[i] == mark and board[6] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[6] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  i+=1
  j+=1
  k+=1
  if board[i] == board[k] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[j] and board[i] == mark and board[k] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[k] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  i+=1
  j+=1
  k+=1
  if board[i] == board[k] and board[i] == mark and board[j] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[i] == board[j] and board[i] == mark and board[k] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[j] == board[k] and board[j] == mark and board[i] == Mark.EMPTY:
    score += (score_mul * possible_end_score)

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # possible diag
  if board[0] == board[8] and board[0] == mark and board[4] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[4] == board[8] and board[4] == mark and board[0] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[0] == board[4] and board[0] == mark and board[8] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[6] == board[4] and board[6] == mark and board[2] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[4] == board[2] and board[4] == mark and board[6] == Mark.EMPTY:
    score += (score_mul * possible_end_score)
  if board[6] == board[2] and board[6] == mark and board[4] == Mark.EMPTY:
    score += (score_mul * possible_end_score)

  # board count
  player_count = 0
  opponent_count = 0
  for i in range(9):
    mark = board[i]
    if mark == Mark.PLAYER:
      player_count += 1
    elif mark == Mark.OPPONENT:
      opponent_count += 1
  score -= (opponent_count * Score.BOARD_COUNT.value)
  score += (player_count * Score.BOARD_COUNT.value)

  return score


def static_evaluation(grid, move, are_max):
  evaluation = 0

  cur_board_num = move.board_num
  cur_board_coord = grid_coord(cur_board_num, 1)
  cur_board = grid[cur_board_coord:cur_board_coord+9]
  evaluation += board_score(cur_board, are_max, False)

  next_board_num = move.cell_num
  next_board_coord = grid_coord(next_board_num, 1)
  next_board = grid[next_board_coord:next_board_coord+9]
  evaluation += board_score(next_board, are_max, True)

  return evaluation

# TODO: consider global board?

def minimax(grid, depth, are_max, cur_board_num, a, b, prev_move):
  possible_moves = get_possible_moves(grid, cur_board_num)
  if have_won(grid, cur_board_num, True):
    return Move(cur_board_num, -1, Score.END.value)
  elif have_won(grid, cur_board_num, False):
    return Move(cur_board_num, -1, -Score.END.value)
  elif (len(possible_moves) == 0):
    return Move(cur_board_num, -1, Score.DRAW.value)
  elif depth == 0:
    score = static_evaluation(grid, prev_move, are_max)
    return Move(cur_board_num, -1, score)

  if are_max:
    max_move = Move(cur_board_num, -1, Score.MIN_SCORE.value)
    for move in possible_moves:
      do_move(grid, move, are_max)
      move_res = minimax(grid, depth-1, False, move.cell_num, a, b, move)
      if move_res.score > max_move.score:
        max_move.score = move_res.score
        max_move.cell_num = move.cell_num
        max_move.board_num = move.board_num
      a = max(max_move.score, a)
      undo_move(grid, move)
      if b <= a:
        break
    return max_move
  else:
    min_move = Move(cur_board_num, -1, Score.MAX_SCORE.value)
    for move in possible_moves:
      do_move(grid, move, are_max)
      move_res = minimax(grid, depth-1, True, move.cell_num, a, b, move)
      if move_res.score < min_move.score:
        min_move.score = move_res.score
        min_move.cell_num = move.cell_num
        min_move.board_num = move.board_num
      b = min(min_move.score, b)
      undo_move(grid, move)
      if b <= a:
        break
    return min_move

def get_possible_moves(grid, cur_board_num):
  moves = []

  for i in range(1, 10):
    coord = grid_coord(cur_board_num, i)
    if grid[coord] == Mark.EMPTY:
      move = Move(cur_board_num, i, 0)
      moves.append(move)

  return moves

def do_move(grid, move, are_max):
  mark = Mark.PLAYER if are_max else Mark.OPPONENT
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = mark 

def undo_move(grid, move):
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = Mark.EMPTY 

def make_move():
  global global_grid
  global global_next_board_num 

  grid_copy = global_grid.copy()

  best_move = minimax(grid_copy, 5, True, global_next_board_num, Score.MIN_SCORE.value, Score.MAX_SCORE.value, None)

  print(f"score={best_move.score}, board={best_move.board_num}, cell={best_move.cell_num}")
  place_mark(global_next_board_num, best_move.cell_num, Mark.PLAYER)

  return best_move.cell_num


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
  port = 0
  if sys.gettrace():
    port = 12345
  else:
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
        print(f"Move: {response}", flush=True)


if __name__ == "__main__":
  main()
