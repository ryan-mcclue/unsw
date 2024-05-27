from collections import deque

def solve_from_cell(hashi_state):
  queue = deque([(0, 0, hashi_state)])  # Start from the top-left corner

    while queue:
      x, y, current_state = queue.popleft()

        if x == current_state.cols:
          x = 0
          y += 1

          if y == current_state.rows:
            return True

        n = get_node(current_state, x, y)

        if not is_island(n) or n.island_count == n.island_lim:
          next_state = copy.deepcopy(hashi_state)
          queue.append((x + 1, y, next_state))
          continue

        for d in Directions:
          if can_place_bridge(current_state, x, y, d):
            next_state = copy.deepcopy(current_state)
            place_bridge(next_state, x, y, d)
            queue.append((x, y, next_state))

    return False

