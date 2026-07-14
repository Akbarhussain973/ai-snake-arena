# ai_minimax.py
# Improved Minimax: always eats adjacent food, strong food drive.

from constants import ALL_DIRS, OPPOSITE, GRID_COLS, GRID_ROWS

class MinimaxAI:
    def __init__(self, snake_id: int):
        self.snake_id = snake_id
        self.difficulty = 0
        self.max_depth = 2

    def set_difficulty(self, level: int):
        self.difficulty = level
        self.max_depth = 2 if level < 2 else 3

    def get_direction(self, head, food, obstacles, other_heads, current_dir):
        # 1. Check immediate food adjacency
        for dx, dy in ALL_DIRS:
            nx, ny = head[0] + dx, head[1] + dy
            if (nx, ny) == food and (nx, ny) not in obstacles:
                return (dx, dy)
        
        # 2. Otherwise use minimax
        best_dir = current_dir
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for next_pos in self._safe_neighbors(head, obstacles, current_dir):
            move = (next_pos[0] - head[0], next_pos[1] - head[1])
            value = self._minimax(
                head=next_pos,
                food=food,
                obstacles=obstacles,
                other_heads=other_heads,
                depth=self.max_depth,
                alpha=alpha,
                beta=beta,
                maximizing=True,
                my_id=self.snake_id
            )
            if value > best_value:
                best_value = value
                best_dir = move
        return best_dir

    def _minimax(self, head, food, obstacles, other_heads, depth, alpha, beta, maximizing, my_id):
        if depth == 0:
            return self._evaluate(head, food, other_heads)

        if maximizing:
            best = -float('inf')
            for nb in self._all_neighbors(head, obstacles):
                val = self._minimax(nb, food, obstacles, other_heads, depth-1, alpha, beta, False, my_id)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            worst = float('inf')
            if other_heads:
                # pick closest opponent for simulation
                opp_head = min(other_heads, key=lambda h: abs(h[0]-head[0]) + abs(h[1]-head[1]))
                for nb in self._all_neighbors(opp_head, obstacles):
                    val = self._minimax(head, food, obstacles, other_heads, depth-1, alpha, beta, True, my_id)
                    worst = min(worst, val)
                    beta = min(beta, worst)
                    if beta <= alpha:
                        break
            else:
                worst = 0
            return worst

    def _evaluate(self, head, food, other_heads):
        # Strong preference for food
        dist = abs(head[0]-food[0]) + abs(head[1]-food[1])
        if dist == 0:
            return 10000
        food_score = 200.0 / (dist + 1)
        # Small penalty near enemies
        enemy_penalty = 0
        for oh in other_heads:
            d = abs(head[0]-oh[0]) + abs(head[1]-oh[1])
            if d < 3:
                enemy_penalty += (3 - d) * 10
        return food_score - enemy_penalty

    def _safe_neighbors(self, head, obstacles, current_dir):
        hx, hy = head
        reverse = OPPOSITE.get(current_dir)
        safe = []
        for dx, dy in ALL_DIRS:
            if (dx, dy) == reverse:
                continue
            nx, ny = hx+dx, hy+dy
            if self._in_bounds(nx, ny) and (nx, ny) not in obstacles:
                safe.append((nx, ny))
        return safe

    def _all_neighbors(self, pos, obstacles):
        px, py = pos
        neigh = []
        for dx, dy in ALL_DIRS:
            nx, ny = px+dx, py+dy
            if self._in_bounds(nx, ny) and (nx, ny) not in obstacles:
                neigh.append((nx, ny))
        return neigh

    def _in_bounds(self, x, y):
        return 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS
    
    