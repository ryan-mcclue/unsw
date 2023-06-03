#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

from binarytree import Node

root = Node(100)
root.left = Node(30)
root.right = Node(20)
root.right.left = Node(6)

root.left.left = Node(10)
root.left.right = Node(5)

print("```", end="")
print(root)
print("```")

root = Node(30)
root.left = Node(10)
root.right = Node(20)
root.right.left = Node(6)

root.left.right = Node(5)

print("```", end="")
print(root)
print("```")
