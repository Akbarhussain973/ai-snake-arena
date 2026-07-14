# ai_astar.py
# A* Pathfinding AI for Snake Arena.
# Finds optimal path to food using A* search.
# Falls back to flood-fill survival move if no path exists.
# Difficulty tunes how far ahead it looks for safe space.

import heapq
from constants import ALL_DIRS, OPPOSITE, GRID_COLS, GRID_ROWS

class AStarAI:
    """
    A* Search:
      - f(n) = g(n) + h(n)
      - g(n) = steps from start (head)
      - h(n) = Manhattan distance to food
      - Avoids all obstacle cells (walls, snake bodies)
      - If no path, uses flood fill to maximize reachable area
    """

    def __init__(self, snake_id: int):
        self.snake_id = snake_id
        self.difficulty = 0      # 0=Easy, 1=Medium, 2=Hard

    def set_difficulty(self, level: int):
        self.difficulty = level

    def get_direction(self, head: tuple, food: tuple, obstacles: set,
                      other_heads: list, current_dir: tuple) -> tuple:
        """
        head        : (x, y) of this snake's head
        food        : (x, y) of current food
        obstacles   : set of blocked cells (walls + other snake bodies)
        other_heads : list of other snakes' heads (not used here but kept for interface consistency)
        current_dir : current direction (to avoid 180° reversal)
        Returns     : direction tuple (dx, dy)
        """
        # Try to find a path to food using A*
        path = self._astar(head, food, obstacles)

        if path and len(path) >= 2:
            next_cell = path[1]
            nx, ny = next_cell
            hx, hy = head
            return (nx - hx, ny - hy)

        # No path to food → survival mode (maximize open space)
        return self._survival_move(head, obstacles, current_dir)

    # ------------------------------------------------------------------
    #  A* Core
    # ------------------------------------------------------------------
    def _astar(self, start: tuple, goal: tuple, obstacles: set) -> list:
        """
        Returns list of (x, y) cells from start to goal (inclusive),
        or empty list if no path exists.
        """
        open_heap = []
        heapq.heappush(open_heap, (0, start))

        came_from = {start: None}
        g_score = {start: 0}

        while open_heap:
            _, current = heapq.heappop(open_heap)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._neighbors(current, obstacles):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._manhattan(neighbor, goal)
                    heapq.heappush(open_heap, (f, neighbor))
                    came_from[neighbor] = current

        return []   # no path found

    def _reconstruct_path(self, came_from: dict, current: tuple) -> list:
        """Reconstruct path from start to current using came_from pointers."""
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def _neighbors(self, pos: tuple, obstacles: set) -> list:
        """Return all adjacent cells that are within bounds and not obstacles."""
        px, py = pos
        result = []
        for dx, dy in ALL_DIRS:
            nx, ny = px + dx, py + dy
            if self._in_bounds(nx, ny) and (nx, ny) not in obstacles:
                result.append((nx, ny))
        return result

    # ------------------------------------------------------------------
    #  Survival Mode (Flood Fill)
    # ------------------------------------------------------------------
    def _survival_move(self, head: tuple, obstacles: set, current_dir: tuple) -> tuple:
        """
        When no path to food exists, pick the direction that maximizes
        reachable open space (flood fill count). Difficulty affects
        how many steps ahead we consider (though here we simply use flood fill).
        """
        reverse = OPPOSITE.get(current_dir)
        best_dir = current_dir
        best_area = -1

        for dx, dy in ALL_DIRS:
            if (dx, dy) == reverse:
                continue
            nx, ny = head[0] + dx, head[1] + dy
            if not self._in_bounds(nx, ny) or (nx, ny) in obstacles:
                continue
            # Compute reachable area from this neighbor
            area = self._flood_fill((nx, ny), obstacles)
            if area > best_area:
                best_area = area
                best_dir = (dx, dy)

        return best_dir

    def _flood_fill(self, start: tuple, obstacles: set) -> int:
        """
        BFS flood fill – returns number of reachable cells from start,
        not counting obstacles.
        """
        visited = {start}
        queue = [start]
        while queue:
            cx, cy = queue.pop()
            for dx, dy in ALL_DIRS:
                nx, ny = cx + dx, cy + dy
                nb = (nx, ny)
                if self._in_bounds(nx, ny) and nb not in obstacles and nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return len(visited)

    # ------------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------------
    def _manhattan(self, a: tuple, b: tuple) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS
    
    