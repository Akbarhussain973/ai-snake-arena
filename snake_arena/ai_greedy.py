# ai_greedy.py
# Greedy Best-First Search AI for Snake Arena.
# Always moves toward the food using Manhattan distance heuristic.
# Falls back to a safe random move if no direct path is possible.
# Difficulty tuning: Higher difficulty = more aggressive (tries to intercept other snakes).

import random
from constants import ALL_DIRS, OPPOSITE, GRID_COLS, GRID_ROWS

class GreedyAI:
    """
    Greedy Best-First Search:
      - Evaluates all four neighbor cells.
      - Picks the one with smallest Manhattan distance to food.
      - Ignores cells that are obstacles (walls, snake bodies).
      - Never reverses direction (no 180° turn).
      - On higher difficulty (level >= 2), it also considers blocking other snakes.
    """

    def __init__(self, snake_id: int):
        self.snake_id = snake_id
        self.difficulty = 0      # 0=Easy, 1=Medium, 2=Hard

    def set_difficulty(self, level: int):
        """Called by DifficultyManager to adjust AI behavior."""
        self.difficulty = level

    def get_direction(self, head: tuple, food: tuple, obstacles: set,
                      other_heads: list, current_dir: tuple) -> tuple:
        """
        head         : (x, y) of this snake's head
        food         : (x, y) of the current food
        obstacles    : set of blocked cells (walls + all snake bodies except own head)
        other_heads  : list of (x,y) for other snakes' heads (alive)
        current_dir  : current direction (to prevent 180° reversal)
        Returns      : direction tuple (dx, dy)
        """
        # Find all safe neighboring cells (not obstacles, not reverse)
        candidates = self._safe_neighbors(head, obstacles, current_dir)

        if not candidates:
            # No safe move – just pick any non-reverse direction (avoid suicide)
            return self._fallback(current_dir)

        if self.difficulty >= 2 and other_heads:
            # Hard mode: try to intercept other snakes
            candidates = self._rank_aggressive(candidates, food, other_heads)
        else:
            # Normal mode: sort by distance to food (closest first)
            candidates.sort(key=lambda pos: self._manhattan(pos, food))

        best = candidates[0]
        bx, by = best
        hx, hy = head
        return (bx - hx, by - hy)

    # ------------------------------------------------------------------
    #  Helper methods
    # ------------------------------------------------------------------
    def _safe_neighbors(self, head: tuple, obstacles: set, current_dir: tuple) -> list:
        """Return list of neighbor positions that are safe to move into."""
        hx, hy = head
        reverse = OPPOSITE.get(current_dir)
        safe = []
        for dx, dy in ALL_DIRS:
            if (dx, dy) == reverse:
                continue
            nx, ny = hx + dx, hy + dy
            if self._in_bounds(nx, ny) and (nx, ny) not in obstacles:
                safe.append((nx, ny))
        return safe

    def _rank_aggressive(self, candidates: list, food: tuple, other_heads: list) -> list:
        """
        For hard difficulty: balance food proximity with intercepting other snakes.
        Score = distance to food - 0.5 * min_distance_to_other_head
        Lower score is better (smaller food distance, smaller distance to other heads).
        """
        def score(pos):
            food_dist = self._manhattan(pos, food)
            # Find closest other snake head
            if other_heads:
                min_enemy_dist = min(self._manhattan(pos, oh) for oh in other_heads)
            else:
                min_enemy_dist = 999
            # We want to be close to food AND close to enemies (to block them)
            # So subtract enemy distance (smaller enemy_dist = better score)
            return food_dist - 0.5 * min_enemy_dist

        return sorted(candidates, key=score)

    def _manhattan(self, a: tuple, b: tuple) -> int:
        """Manhattan distance between two grid cells."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS

    def _fallback(self, current_dir: tuple) -> tuple:
        """Emergency move: choose any direction that is not the opposite of current_dir."""
        reverse = OPPOSITE.get(current_dir)
        dirs = [d for d in ALL_DIRS if d != reverse]
        return random.choice(dirs) if dirs else (1, 0)  # fallback to RIGHT