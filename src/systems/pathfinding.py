import heapq

def chebyshev_distance(col_a, row_a, col_b, row_b):
    """
    Chebyshev distance — the number of steps a king takes on a chessboard.
    Used as the A* heuristic for grid-based movement.
    Accounts for diagonal movement costing the same as cardinal movement.
    """
    return max(abs(col_a - col_b), abs(row_a - row_b))

def astar(start_col, start_row, goal_col, goal_row, room):
    """
    A* pathfinding algorithm contained within a single room's tile grid.
    Finds the shortest walkable path from start to goal.

    Returns a list of (col, row) tuples representing the path
    from start to goal inclusive, or an empty list if no path exists.

    Uses Chebyshev distance as the heuristic.
    Diagonal movement is allowed.
    """
    # Each entry in the heap is (f_score, col, row)
    open_heap = []
    heapq.heappush(open_heap, (0, start_col, start_row))

    # Track where each node came from for path reconstruction
    came_from = {}

    # Cost from start to each node
    g_score = {(start_col, start_row): 0}

    # Estimated total cost through each node
    f_score = {(start_col, start_row): chebyshev_distance(
        start_col, start_row, goal_col, goal_row
    )}

    while open_heap:
        _, current_col, current_row = heapq.heappop(open_heap)

        # Reached the goal — reconstruct and return the path
        if current_col == goal_col and current_row == goal_row:
            return reconstruct_path(came_from, current_col, current_row)

        # Check all 8 neighbours (cardinal + diagonal)
        for d_col, d_row in [
            (0, -1), (0, 1), (-1, 0), (1, 0),    # cardinal
            (-1, -1), (-1, 1), (1, -1), (1, 1)   # diagonal
        ]:
            neighbour_col = current_col + d_col
            neighbour_row = current_row + d_row

            # Skip tiles that are not walkable
            # Goal tile is always considered walkable so enemies
            # can path to the player's position
            if (neighbour_col != goal_col or neighbour_row != goal_row):
                if not room.tiles[neighbour_row][neighbour_col].walkable \
                   if 0 <= neighbour_row < room.height \
                   and 0 <= neighbour_col < room.width \
                   else True:
                    continue

            # Skip out of bounds
            if not (0 <= neighbour_row < room.height and
                    0 <= neighbour_col < room.width):
                continue

            tentative_g = g_score[(current_col, current_row)] + 1

            if tentative_g < g_score.get((neighbour_col, neighbour_row), float("inf")):
                came_from[(neighbour_col, neighbour_row)] = (current_col, current_row)
                g_score[(neighbour_col, neighbour_row)]   = tentative_g
                f_score[(neighbour_col, neighbour_row)]   = (
                    tentative_g +
                    chebyshev_distance(neighbour_col, neighbour_row, goal_col, goal_row)
                )
                heapq.heappush(open_heap, (
                    f_score[(neighbour_col, neighbour_row)],
                    neighbour_col,
                    neighbour_row
                ))

    # No path found
    return []

def reconstruct_path(came_from, end_col, end_row):
    """
    Walks backward through came_from to reconstruct
    the full path from start to goal.
    Returns the path as a list of (col, row) tuples.
    """
    path    = [(end_col, end_row)]
    current = (end_col, end_row)

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path