#**********************************************************************
#   search.py
#
#   UNSW CSE
#   COMP3411/9814
#   Code for Path Search Algorithms
#
import numpy as np
import random
import argparse

from node_heap import Node, MyHeap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--s',type=str,default='bfs',
                        help= 'bfs,bfs1,ucs,dfs,greedy,astar or heuristic')
    parser.add_argument('--id',action='store_true',default=False,
                        help='iterative deepening')
    parser.add_argument('--w',type=float,default=1.0,
                        help='weight for heuristic search')
    parser.add_argument('--env',type=str,default='sliding',
                        help='sliding, romania or graph')
    parser.add_argument('--rows',type=int,default=4,
                        help='rows in sliding tile puzzle')
    parser.add_argument('--cols',type=int,default=0,
                        help='cols in sliding tile puzzle')
    parser.add_argument('--d',type=int,default=10,
                        help='depth of (random) initial state')
    parser.add_argument('--start',type=str,default=None,help='start state')
    parser.add_argument('--goal',type=str,default=None,help='goal state')
    parser.add_argument('--v',action='store_true',default=False,help='verbose')
    parser.add_argument('--unique',action='store_true',default=False,
                        help='print each expanded state only once')
    parser.add_argument('--shuffle',action='store_true',default=False,
                        help='shuffle generated nodes in random order')
    args = parser.parse_args()

    if args.env == 'sliding':
        from sliding import State
    elif args.env == 'romania':
        from romania import State
    elif args.env == 'graph':
        from graph   import State
    else:
        print('Unknown Environment:',args.env)
        exit(1)

    start_state = State.start_state(args)

    if not args.goal is None:
        State.set_goal(args.goal)
    
    print('Start:',end='')
    start_state.print_state()
    print()
    start = Node(start_state,None,None,0,0,args.s,args.w)
    num_expand = 0
    solved = False

    if args.s == 'dfs' and not args.id:  # non-iterative depth first search
        num_expand = search(start,args,1000000,num_expand)

    elif( args.id ):                     # iterative deepening search
        for max_cost in range(2,1000000,2):
            print('limit:',max_cost,end='.')
            num_expand = search(start,args,max_cost,num_expand)
            print(' Expanded:',num_expand)
    else:
        heap = MyHeap(args.s)
        heap.insert(start)
        while heap.size > 0 and not solved:
            num_expand += 1
            node = heap.remove_min()
            if args.v:
                node.print_node_ghf(args,args.unique)
            if num_expand % 1000 == 0:
                print(num_expand)
            if( node.state.is_goal()):
                solved = True
                print_solution(node,num_expand,args)
            else:
                generate_and_expand(node,args,0,num_expand,heap)

#**********************************************************************
#  Search recursively, until goal is reached or max_cost is exceeded.
#  Return the total number of nodes expanded.
#
def search( node, args, max_cost, num_expand=0 ):
    num_expand += 1
    if args.v:
        node.print_node_ghf(args,args.unique)
    if( node.state.is_goal()):
        solved = True
        print_solution(node,num_expand,args)
        exit(1)
    else:
        return generate_and_expand(node,args,max_cost,num_expand,None)

#**********************************************************************
#  Generate all children of the specified node, check for goal,
#  and either add to heap or search recursively.
#
def generate_and_expand( node, args, max_cost=0, num_expand=0, heap=None ):
    children = node.state.expand()
    if args.shuffle:
        random.shuffle(children)
    for (state,act,cost) in children:
        if (args.s == 'bfs' or args.s == 'dfs') and state.is_goal():
            child = Node(state,node,act,node.depth+1,node.g+cost,args.s,args.w)
            print_solution(child,num_expand,args)
            exit(1)
        elif not ancestor_of(state,node):
            child = Node(state,node,act,node.depth+1,node.g+cost,args.s,args.w)
            if args.id or args.s == 'dfs':     # search recursively
                if child.cost <= max_cost:
                    num_expand = search(child,args,max_cost,num_expand)
            else:
                heap.insert(child)
    return num_expand
                
#**********************************************************************
#  Return True if state is an ancestor of node; False otherwise.
#
def ancestor_of( state, node ):
    ancestor = node
    while not (ancestor is None or ancestor.state.is_equal_to(state)):
        ancestor = ancestor.parent
    return( not ancestor is None)

#**********************************************************************
#   Print the path that was found.
#
def print_solution( node, num_expand, args ):
    node.print_path()
    print()
    if args.s == 'heuristic':
        print('[w=',args.w,end='')
    else:
        print('[',end='')
        print(args.s,end='')
    if args.id:
        print(',id',end='')
    print(']',end=' ')
    print('Generated:',Node.tick,end='.')
    print(' Expanded:',num_expand,end='.')
    print(' Length:',node.depth,end='.')
    print(' Cost:',node.g,end='.')
    print()


if __name__ == '__main__':
    main()

