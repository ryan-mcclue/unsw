#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import sys
import socket
import random
import copy

from dataclasses import dataclass, field
from typing import List
from enum import Enum

import sys

class Mark(Enum):
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

class Score(Enum):
  END = 15
  # TODO(Ryan): Maybe make draw negative?
  DRAW = -100
  LONE = 1
  POSSIBLE_END = 2

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

#  . . . | . . . | . . .
#  . . . | . . . | . . .
#  . . O | . . . | . . .
#  ------+-------+------
#  . . . | . . . | . . .
#  . . . | . . . | . . .
#  . . . | . . . | X . .
#  ------+-------+------
#  . . . | X . . | . . .
#  . . . | . . . | . X .
#  . . O | . . . | . O X
def pc(i):
  global global_grid
  if global_grid[i] == Mark.EMPTY:
    return '.'
  elif global_grid[i] == Mark.PLAYER:
    return 'O'
  else:
    return 'X'

def print_board():
  global global_grid

  print(f" {pc(0)} {pc(1)} {pc(2)} | {pc(9)} {pc(10)} {pc(11)} | {pc(18)} {pc(19)} {pc(20)}")
  print(f" {pc(3)} {pc(4)} {pc(5)} | {pc(12)} {pc(13)} {pc(14)} | {pc(21)} {pc(22)} {pc(23)}")
  print(f" {pc(6)} {pc(7)} {pc(8)} | {pc(15)} {pc(16)} {pc(17)} | {pc(24)} {pc(25)} {pc(26)}")
  print(f" ------+-------+------")
  print(f" {pc(27)} {pc(28)} {pc(29)} | {pc(36)} {pc(37)} {pc(38)} | {pc(45)} {pc(46)} {pc(47)}")
  print(f" {pc(30)} {pc(31)} {pc(32)} | {pc(39)} {pc(40)} {pc(41)} | {pc(48)} {pc(49)} {pc(50)}")
  print(f" {pc(33)} {pc(34)} {pc(35)} | {pc(42)} {pc(43)} {pc(44)} | {pc(51)} {pc(52)} {pc(53)}")
  print(f" ------+-------+------")
  print(f" {pc(54)} {pc(55)} {pc(56)} | {pc(63)} {pc(64)} {pc(65)} | {pc(72)} {pc(73)} {pc(74)}")
  print(f" {pc(57)} {pc(58)} {pc(59)} | {pc(66)} {pc(67)} {pc(68)} | {pc(75)} {pc(76)} {pc(77)}")
  print(f" {pc(60)} {pc(61)} {pc(62)} | {pc(69)} {pc(70)} {pc(71)} | {pc(78)} {pc(79)} {pc(80)}")

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

def could_win(grid, board, mark):
  row_indices = [[0,1,2],[0,2,1],[1,2,0],
                 [3,4,5],[3,5,4],[4,5,3],
                 [6,7,8],[6,8,7],[7,8,6]]
  for indexes in row_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True

  col_indices = [[0,3,6],[3,6,0],[0,6,3],
                 [1,4,7],[4,7,1],[1,7,4],
                 [2,5,8],[5,8,2],[2,8,5]]
  for indexes in col_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True

  diag_indices = [[0,4,8],[4,8,0],[0,8,4],
                  [6,4,2],[6,2,4],[4,2,6]]
  for indexes in diag_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True
   
  return False

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

def score_one_mark_remaining(board, are_max, is_next):
  score = 0
  
  next_mark = Mark.OPPONENT if are_max else Mark.PLAYER

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # IMPORTANT: format is [m,m,e]
  row_indices = [[0,1,2],[0,2,1],[1,2,0],
                 [3,4,5],[3,5,4],[4,5,3],
                 [6,7,8],[6,8,7],[7,8,6]]
  col_indices = [[0,3,6],[3,6,0],[0,6,3],
                 [1,4,7],[4,7,1],[1,7,4],
                 [2,5,8],[5,8,2],[2,8,5]]
  diag_indices = [[0,4,8],[4,8,0],[0,8,4],
                  [6,4,2],[6,2,4],[4,2,6]]

  for direction_indices in [row_indices, col_indices, diag_indices]:
    for indices in direction_indices:
      i, j, k = indices
      if board[i] == board[j] and board[k] == Mark.EMPTY:
        if board[i] == Mark.PLAYER:
          if is_next and next_mark == Mark.PLAYER:
            score += Score.END.value 
          else:
            score += Score.POSSIBLE_END.value 
            break
        elif board[i] == Mark.OPPONENT:
          if is_next and next_mark == Mark.OPPONENT:
            score -= Score.END.value 
          else:
            score -= Score.POSSIBLE_END.value 
            break

  return score

def score_lone_mark(board):
  score = 0

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # IMPORTANT: format is [m,e,e]
  row_indices = [[0,1,2],[1,0,2],[2,0,1],
                 [3,4,5],[4,3,5],[5,3,4],
                 [6,7,8],[7,6,8],[8,6,7]]
  col_indices = [[0,3,6],[3,0,6],[6,0,3],
                 [1,4,7],[4,1,7],[7,1,4],
                 [2,5,8],[5,2,8],[8,2,5]]
  diag_indices = [[0,4,8],[4,8,0],[8,0,4],
                  [6,4,2],[4,6,2],[2,4,6]]

  for direction_indices in [row_indices, col_indices, diag_indices]:
    for indices in direction_indices:
      i, j, k = indices
      if board[j] == Mark.EMPTY and board[k] == Mark.EMPTY:
        if board[i] == Mark.PLAYER:
          score += Score.LONE.value
        elif board[i] == Mark.OPPONENT:
          score -= Score.LONE.value

  return score

def board_score(board, are_max, is_next):
  score = 0
  
  score += score_one_mark_remaining(board, are_max, is_next)
  score += score_lone_mark(board)

  return score


def static_evaluation(grid, are_max, prev_move):
  evaluation = 0
  #for i in range(1, 10):
  #  board_coord = grid_coord(i, 1)
  #  board = grid[board_coord:board_coord+9]
  #  evaluation += board_score(board, are_max, i == prev_move.cell_num)
  #return evaluation

  cur_board_coord = grid_coord(prev_move.board_num, 1)
  cur_board = grid[cur_board_coord:cur_board_coord+9]
  evaluation += board_score(cur_board, are_max, False)

  next_board_coord = grid_coord(prev_move.cell_num, 1)
  next_board = grid[next_board_coord:next_board_coord+9]
  evaluation += board_score(next_board, are_max, True)
    

  return evaluation

MAX_DEPTH = 6

def minimax(grid, depth, are_max, cur_board_num, a, b, prev_move):
  if depth == MAX_DEPTH:
    return static_evaluation(grid, are_max, prev_move)

  # TODO: perhaps check if won here; just have to check all boards?

  scores = []

  possible_moves = get_possible_moves(grid, cur_board_num, are_max)

  for move in possible_moves:
    do_move(grid, move, are_max) 

    if have_won(grid, cur_board_num, True):
      score = Score.END.value - depth
    elif have_won(grid, cur_board_num, False):
      score = depth - Score.END.value
    else:
      score = minimax(grid, depth+1, not are_max, move.cell_num, a, b, move)

    undo_move(grid, move)

    if are_max:
      a = max(a, score)
    else:
      b = min(b, score)

    if b <= a:
      break

    if depth == 0:
      scores.append([move, score])
    else:
      scores.append(score)

  # if a draw
  if len(scores) == 0:
    return Score.DRAW.value

  if depth == 0:
    if are_max:
      return max(scores, key=lambda x: x[1])[0]
    else:
      return min(scores, key=lambda x: x[1])[0]
  else:
    if are_max:
      return max(scores)
    else:
      return min(scores)


def have_tie(grid, board_num):
  coord = grid_coord(board_num, 1)
  for i in range(9):
    if grid[coord + i] == Mark.EMPTY:
      return False
  return True

def get_possible_moves(grid, board_num, are_max):
  moves = []
  coord = grid_coord(board_num, 1)
  board = grid[coord:coord+9]

  numbers = list(range(1, 10))
  random.shuffle(numbers)

  for i in numbers:
    if board[i-1] == Mark.EMPTY and not have_tie(grid, i):
      move = Move(board_num, i, 0)
      moves.append(move)
  return moves

  # moves = []
  # losable_moves = []

  # coord = grid_coord(board_num, 1)
  # board = grid[coord:coord+9]
  # 
  # for i in range(1, 10):
  #   if board[i-1] == Mark.EMPTY and not have_tie(grid, i):
  #     next_coord = grid_coord(i, 1)
  #     next_board = grid[next_coord:next_coord+9]
  #     # if we win
  #     if other_can_win(board, not are_max):
  #       return [Move(board_num, i, 0)]
  #     elif other_can_win(next_board, are_max):
  #       losable_moves.append(Move(board_num, i, 0))
  #     else:
  #       move = Move(board_num, i, 0)
  #       moves.append(move)

  # if len(moves) == 0:
  #   return losable_moves
  # else:
  #   return moves

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

  best_move = minimax(global_grid, 0, True, global_next_board_num, Score.MIN_SCORE.value, Score.MAX_SCORE.value, None)

  place_mark(global_next_board_num, best_move.cell_num, Mark.PLAYER)

  return best_move.cell_num


global_moves_to_choose = []

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
    print_board()
    return -1
  elif command == "loss":
    print("We lost :(")
    print_board()
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

# TODO: undo() not making empty?
#class Board:
#  char board[9],
#  x_indexes, (so, what moves have been made)
#  o_indexes
#
#class State:
#  Board boards[9]
#  diff = 7
#  tie_boards, x_chosen_board, o_chosen_board
#
#
#def study():
#  pc_grid = 0
#  pc_cell = 0
#  play(pc_grid, pc_cell, turn=1)
#  
#  checkerboard: (checking if board closed)
#  for (b in boards)
#    if b.score == 0: tie_boards[board] = 1
#    if b.score == 1: x_win_boards[board] = 1
#    if b.score == -1: o_win_boards[board] = 1
#    else tie/x/o_boards[board] = -1
#
#  check_if_won()
#
#  for (cell in empty_cells_in_board)
#    v = minmax(board, cell, depth=6, a, b, turn)
#    undo_move()
#
#def eval():
#  for i, b in enumerate(boards):
#    if x_won(b):
#      scores[i] = 15
#    if o_won(b)
#      scores[i] = -15
#    if tie(b):
#      scores[i] = -99999
#    else:
#      scores[i] = calc_small(); 
#
#  return sum_of_all_non_tie_scores
#
#def calc_small():
#  avg = 0
#  for c in board:
#    if c is x: scores[i] = 1
#    if c is o: scores[i] = -1
#    else scores[i] = 0
#
#    for all x.x avg += 2
#    if b[0] == x:
#      if b[1] == x or b[2] == x: avg += 2
#
#    for all .x. avg += 1
#
#    repeat for o, i.e. negative scores
