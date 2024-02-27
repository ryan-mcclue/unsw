#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

# 1. Reduce to solving for smallest element, i.e. a base
# 2. Iterate over all possible choices for element:
#    If choice valid, recurse on moving along, else undo
# 3. If x overflow, update to new location
#    If y overflow, know have reached goal state

def solve_hashi(hashi_state):
  return solve_from_cell(hashi_state, 0, 0)

def solve_from_cell(hashi_state, x, y):
  # goal state is when solved last item
  if x == hashi_state.cols:
    x = 0
    y += 1
    if y == hashi_state.rows:
      return True

  n = get_node(hashi_state, x, y)
  if not is_base(n):
    return solve_from_cell(hashi_state, x + 1, y)
  elif n.base_count == n.base_lim:
    return solve_from_cell(hashi_state, x + 1, y)

  # this for loop is for exploration
  for d in Directions:
    if can_place_bridge(hashi_state, x, y, d):
      place_bridge(hashi_state, x, y, d)
      if solve_from_cell(x, y):
        return True
      else:
        # remove decision if coming up
        remove_bridge(hashi_state, x, y, d)

  return False
