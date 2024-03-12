#**********************************************************************
#   graph.py
#
#   UNSW CSE
#   COMP3411/9814
#   This code presents the graph search problem from the Week 3 Tutorial
#   in a format used by the path search algorithms implemented in search.py

import numpy as np
import random

adjacent = {
    'A':[('B',2),('C',2),('D',4),('S',2),('T',6)],
    'B':[('A',2),('T',5)],
    'C':[('A',2),('D',2),('S',3),('U',3),('X',5)],
    'D':[('A',4),('C',2),('T',4),('X',2)],
    'E':[('F',3),('W',4)],
    'F':[('E',3),('G',3),('W',2),('Y',2),('Z',2)],
    'G':[('F',3),('Z',3)],
    'S':[('A',2),('C',3)],
    'T':[('A',6),('B',5),('D',4),('V',1),('X',2)],
    'U':[('C',3),('W',5),('X',2)],
    'V':[('T',1),('X',3),('Z',4)],
    'W':[('E',4),('F',2),('U',5),('X',3),('Y',2)],
    'X':[('C',5),('D',2),('T',2),('U',2),('V',3),('W',3),('Y',4),('Z',6)],
    'Y':[('F',2),('W',2),('X',4),('Z',3)],
    'Z':[('F',2),('G',3),('V',4),('X',6),('Y',3)]}

heuristic = {'A':9,'B':7,'C':7,'D':7,'E':4,'F':3,'G':0,
             'S':9,'T':8,'U':7,'V':7,'W':2,'X':5,'Y':5,'Z':1}

class State:

    goal = 'G'
    
    def __init__(self,a='S'):
        self.a = a
        self.h = heuristic[a]
        
    def start_state(args):
        if args.start is None:
            return State('S')
        else:
            return State(args.start)
        
    def set_goal(goal):
        State.goal = goal
    
    def is_equal_to(self,other):
        return(self.a == other.a)

    def expand( self ):
        children = []
        for (state,cost) in adjacent[self.a]:
            children.append((State(state),'-',cost))
        return children

    def is_goal( self ):
        return self.a == State.goal

    def heuristic( self ):
        return heuristic[self.a]
        
    def print_action(self,action):
        print('->',end='')

    def print_state(self):
        print(self.a,end='')
