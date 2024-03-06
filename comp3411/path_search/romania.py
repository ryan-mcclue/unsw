#**********************************************************************
#   romania.py
#
#   UNSW CSE
#   COMP3411/9814
#   This code presents the Romania map problem in a format that can be
#   used by the path search algorithms implemented in search.py

import numpy as np
import random

adjacent = {
    'arad':[('sibiu',140),('timisoara',118),('zerind',75)],
    'bucharest':[('fagaras',211),('giurgiu',90),
                 ('pitesti',101),('urziceni',85)],
    'craiova':[('dobreta',120),('pitesti',138),('rimnicu vilcea',146)],
    'dobreta':[('craiova',120),('mehadia',75)],
    'eforie':[('hirsova',86)],
    'fagaras':[('bucharest',211),('sibiu',99)],
    'giurgiu':[('bucharest',90)],
    'hirsova':[('eforie',86),('urziceni',98)],
    'iasi':[('neamt',87),('vaslui',92)],
    'lugoj':[('mehadia',70),('timisoara',111)],
    'mehadia':[('dobreta',75),('lugoj',70)],
    'neamt':[('iasi',87)],
    'oradea':[('sibiu',151),('zerind',71)],
    'pitesti':[('bucharest',101),('craiova',138),('rimnicu vilcea',97)],
    'rimnicu vilcea':[('craiova',146),('pitesti',97),('sibiu',80)],
    'sibiu':[('arad',140),('fagaras',99),('oradea',151),('rimnicu vilcea',80)],
    'timisoara':[('arad',118),('lugoj',111)],
    'urziceni':[('bucharest',85),('hirsova',98),('vaslui',142)],
    'vaslui':[('iasi',92),('urziceni',142)],
    'zerind':[('arad',75),('oradea',71)]}

heuristic = {
    'arad':366,'bucharest':0,'craiova':160,'dobreta':242,
    'eforie':161,'fagaras':178,'giurgiu':77,'hirsova':151,
    'iasi':226,'lugoj':244,'mehadia':241,'neamt':234,
    'oradea':380,'pitesti':98,'rimnicu vilcea':193,'sibiu':253,
    'timisoara':329,'urziceni':80,'vaslui':199,'zerind':374}

class State:

    goal = 'bucharest'
    
    def __init__(self,a='arad'):
        self.a = a
        self.h = heuristic[a]
        
    def start_state(args):
        if args.start is None:
            return State('arad')
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
