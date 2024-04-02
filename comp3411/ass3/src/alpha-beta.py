#**********************************************************
#   ttt.py
#
#   UNSW CSE
#   COMP3411/9814
#   Code for Tic-Tac-Toe with Alpha-Beta search
#
import numpy as np

EMPTY = 2

ILLEGAL_MOVE  = 0
STILL_PLAYING = 1
WIN           = 2
LOSS          = 3
DRAW          = 4

MAX_MOVE      = 9

MIN_EVAL = -1000000
MAX_EVAL =  1000000

def main():
    board = EMPTY*np.ones(10,dtype=np.int32)
    move = np.zeros(10,dtype=np.int32)
    best_move = np.zeros(10,dtype=np.int32)
    is_human = (True,False)
    game_status = STILL_PLAYING
    player = 1
    m = 0

    while m < MAX_MOVE and game_status == STILL_PLAYING:
        m += 1
        player = 1-player;
        if is_human[player]:
            print_board( board )
            move[m] = input('Enter move [1-9]: ')
            while move[m] < 1 or move[m] > 9 or board[move[m]] != EMPTY:
                move[m] = input('Enter move [1-9]: ')
        else:
            alphabeta( player,m,board,MIN_EVAL,MAX_EVAL,best_move )
            move[m] = best_move[m];
        game_status = make_move( player, m, move, board )

    print_board( board )

#**********************************************************
#   Print the board
#
def print_board( bd ):
    sb = 'XO.'
    print('|',sb[bd[1]],sb[bd[2]],sb[bd[3]],'|')
    print('|',sb[bd[4]],sb[bd[5]],sb[bd[6]],'|')
    print('|',sb[bd[7]],sb[bd[8]],sb[bd[9]],'|')

#**********************************************************
#   Negamax formulation of alpha-beta search
#
def alphabeta( player, m, board, alpha, beta, best_move ):

    best_eval = MIN_EVAL;

    if game_won( 1-player, board ):   # LOSS
        return -1000 + m; # better to win faster (or lose slower)

    this_move = 0;
    for r in range( 1, 10):
        if board[r] == EMPTY:         # move is legal
            this_move = r
            board[this_move] = player # make move
            this_eval = -alphabeta(1-player,m+1,board,-beta,-alpha,best_move)
            board[this_move] = EMPTY; # undo move
            if this_eval > best_eval:
                best_move[m] = this_move;
                best_eval = this_eval
                if best_eval > alpha:
                    alpha = best_eval
                    if alpha >= beta: # cutoff
                        return( alpha )

    if this_move == 0:  # no legal moves
        return( 0 )     # DRAW
    else:
        return( alpha )

#**********************************************************
#   Make specified move on the board and return game status
#
def make_move( player, m, move, board ):
    if board[move[m]] != EMPTY:
        print('Illegal Move')
        return ILLEGAL_MOVE
    else:
        board[move[m]] = player
        if game_won( player, board ):
            return WIN
        elif full_board( board ):
            return DRAW
        else:
            return STILL_PLAYING

#**********************************************************
#   Return True if the board is full
#
def full_board( board ):
    b = 1
    while b <= 9 and board[b] != EMPTY:
        b += 1
    return( b == 10 )

#**********************************************************
#   Return True if game won by player p on board bd[]
#
def game_won( p, bd ):
    return(  ( bd[1] == p and bd[2] == p and bd[3] == p )
           or( bd[4] == p and bd[5] == p and bd[6] == p )
           or( bd[7] == p and bd[8] == p and bd[9] == p )
           or( bd[1] == p and bd[4] == p and bd[7] == p )
           or( bd[2] == p and bd[5] == p and bd[8] == p )
           or( bd[3] == p and bd[6] == p and bd[9] == p )
           or( bd[1] == p and bd[5] == p and bd[9] == p )
           or( bd[3] == p and bd[5] == p and bd[7] == p ))

if __name__ == '__main__':
    main()

