#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

from binarytree import Node

root = Node(0)
root.left = Node(0)
root.right = Node(0)

min_l = Node(0)
min_l.left = Node(0)
min_l.right = Node(0)

max_ll = Node(0)
max_ll.left = Node(0)
max_ll.right = Node(0)
max_rr = Node(0)
max_rr.left = Node(0)
max_rr.right = Node(0)

min_lll = Node(0)
min_lll.left = Node(0)
min_lll.right = Node(0)
min_rrr = Node(0)
min_rrr.left = Node(0)
min_rrr.right = Node(0)

max_ll.left = min_lll
max_ll.right = min_rrr
max_rr.left = min_lll
max_rr.right = min_rrr

min_l.left = max_ll
min_l.right = max_rr

root.left = min_l
root.right = min_l



print("```", end="")
print(root)
print("```")
