#**********************************************************************
#   node_heap.py
#
#   UNSW CSE
#   COMP3411/9814
#   This code provides the Node and Heap classes which are used
#   by the path search algorithms implemented in search.py
#

class Node:

    tick = 0
    printed = []

    def __init__(self, state, parent=None, action=None,
                 depth=0, g=0, strategy='bfs', weight=1 ):
        self.state  = state
        self.parent = parent
        self.action = action
        self.depth  = depth
        self.g      = g
        self.cost   = self.get_cost(strategy,weight)
        self.num    = Node.tick
        Node.tick += 1

    def get_cost( self, strategy, weight ):
        if strategy == 'bfs' or strategy == 'bfs1' or strategy == 'dfs':
            return  self.depth
        elif strategy == 'ucs':
            return  self.g
        elif strategy == 'greedy':
            return  self.state.h
        elif strategy == 'astar':
            return self.g + self.state.h
        elif strategy == 'heuristic':
            return (2-weight)*self.g + weight*self.state.h
        else:
            print('Unknown Strategy: ',strategy)
            exit( 1 )

    def print_state(self):
        for k in range(self.depth):
            print('.',end='')
        print(' ',end='')
        self.state.print_state()

    def print_path(self):
        if self.parent is None:
            self.state.print_state()
        else:
            self.parent.print_path()
            self.state.print_action(self.action)
            self.state.print_state()

    def print_node_ghf(self,args,unique=False):
        if unique:
            for state in Node.printed:
                if self.state.is_equal_to(state):
                    return
            Node.printed.append(self.state)
        self.print_state()
        if args.s == 'ucs' or args.s == 'astar' or args.s == 'heuristic':
            print(' (g:',end='')
            print(self.g,end='')
            if args.s == 'astar' or args.s == 'heuristic':
                print(', h:',end='')
                print(self.state.h,end='')
                print(', f:',end='')
                print(self.cost,end='')
            print(')',end='')
        print()

    
#**********************************************************************
#   Priority Queue implemented as a Heap. When two nodes rank equally,
#   priority is given to the one generated earlier.
#
class MyHeap:
    def __init__(self,strategy='bfs',weight=1):
        self.a = [0]
        self.size = 0
        self.strategy = strategy
        self.weight = weight

    def sift_up(self,i):
        keep_going = True
        while i//2 > 0 and keep_going:
            diff = self.a[i].cost - self.a[i//2].cost
            if diff < 0 or ( diff == 0 and self.a[i].num < self.a[i//2].num ):
                tmp = self.a[i]
                self.a[i] = self.a[i//2]
                self.a[i//2] = tmp
            else:
                keep_going = False
            i = i//2

    def insert(self,n):
        self.a.append(n)
        self.size += 1
        self.sift_up(self.size)

    def sift_down(self, i):
        while (i*2) <= self.size:
            mc = self.min_child(i)
            diff = self.a[i].cost - self.a[mc].cost
            if diff > 0 or ( diff == 0 and self.a[i].num > self.a[mc].num ):
                tmp = self.a[i]
                self.a[i] = self.a[mc]
                self.a[mc] = tmp
            i = mc

    def min_child(self, i):
        if (i*2)+1 > self.size:
            return i*2
        else:
            diff = self.a[i*2].cost - self.a[(i*2)+1].cost
            if   diff <  0 or \
               ( diff == 0 and self.a[i*2].num < self.a[(i*2)+1].num ):
                return i*2
            else:
                return (i*2)+1

    def remove_min(self):
        if len(self.a) == 1:
            return None
        root = self.a[1]
        last = self.a.pop()
        if self.size > 1:
            self.a[1] = last
        self.size -= 1
        self.sift_down(1)
        return root

