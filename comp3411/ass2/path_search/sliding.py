#**********************************************************************
#   sliding.py
#
#   UNSW CSE
#   COMP3411/9814
#   This code presents the sliding tile puzzle in a format used by the
#   path search algorithms implemented in search.py

import numpy as np
import random

class State:

    def __init__(self,a,rows=3,cols=0):
        self.a = a
        self.rows = rows
        if cols == 0:
            self.cols = self.rows
        else:
            self.cols = cols
        self.h = self.heuristic()

    def start_state(args):
        if args.start is None:
            state = State.goal_state(args.rows,args.cols)
            for k in range(args.d):
                children = state.expand()
                (state,act,cost) = random.choice(children)
            return state
        elif args.start == 'tutorial':
            return State(np.array([1,2,3,8,5,0,4,7,6]),3)
        else:
            list = []
            for ch in args.start:
                n = ord(ch)
                if n >= 48 and n <= 57:    # '0' to '9'
                    list.append(n - 48)
                elif n >= 65 and n <= 90:  # 'A' to 'Z'
                    list.append(n - 55)
                elif n >= 97 and n <= 122: # 'a' to 'z'
                    list.append(n - 87)
            if len(list) == 6:
                row = 2
                col = 3
            elif len(list) == 9:
                row = 3
                col = 3
            elif len(list) == 12:
                row = 3
                col = 4
            elif len(list) == 16:
                row = 4
                col = 4
            else:
                print('Scanned',len(list),'tiles.')
                exit(1)
            return(State(np.array(list),row,col))

    def goal_state(rows=3,cols=0):
        if cols == 0:
            cols = rows
        a = np.arange(1,(rows*cols)+1)
        a[(rows*cols)-1] = 0
        return State(a,rows,cols)

    def is_equal_to(self,other):
        return(np.array_equal(self.a, other.a))
    
    def expand( self ):
        children = []
        r = self.rows
        c = self.cols
        k = np.where(self.a == 0)[0][0]
        if k < (r-1)*c:
            a1 = self.a.copy()
            a1[k] = self.a[k+c]
            a1[k+c] = 0
            s1 = State(a1,r,c)
            children.append((s1,'down',1))
        if (k % c) < c-1:
            a1 = self.a.copy()
            a1[k] = self.a[k+1]
            a1[k+1] = 0
            s1 = State(a1,r,c)
            children.append((s1,'right',1))
        if k % c > 0:
            a1 = self.a.copy()
            a1[k] = self.a[k-1]
            a1[k-1] = 0
            s1 = State(a1,r,c)
            children.append((s1,'left',1))
        if k >= c:
            a1 = self.a.copy()
            a1[k] = self.a[k-c]
            a1[k-c] = 0
            s1 = State(a1,r,c)
            children.append((s1,'up',1))
        return children

    def is_goal( self ):
        r = self.rows
        c = self.cols
        for k in range((r*c)-1):
            if self.a[k] != k+1:
                return False
        return True

    def heuristic( self ):
        return self.man_dist()
        
    def man_dist( self ):
        r = self.rows
        c = self.cols
        dist = 0
        for j in range(0,r*c):
            k = self.a[j]-1
            if k >= 0:
                dist = dist + abs(k%c - j%c) + abs(k//c - j//c)
        return dist

    def print_action(self,action):
        print(' (',action,')')

    def print_state(self):
        r = self.rows
        c = self.cols
        for i in range(r):
            if i > 0:
                print('-',end='')
            for j in range(c):
                k = self.a[(i*c)+ j]
                if k < 10:
                    print(k,end='')
                else:
                    print(chr(k+55),end='')

