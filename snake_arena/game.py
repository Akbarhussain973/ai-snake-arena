# game.py (respects enabled_ai_ids)
import random
from constants import (
    GRID_COLS, GRID_ROWS, PLAYER_ID, ASTAR_ID, GREEDY_ID, MINIMAX_ID,
    RIGHT, LEFT, DOWN, UP, GOLDEN_FOOD_ENABLED, FOOD_COUNT_FOR_GOLDEN,
    GOLDEN_SCORE_MULTIPLIER, GOLDEN_DURATION_FRAMES
)
from snake import Snake
from maps import get_map

class Game:
    EMPTY = 0
    FOOD = 1
    GOLDEN_FOOD = 2

    def __init__(self, mode="pvai", map_name="classic", player_name="Player", enabled_ai_ids=None):
        self.mode = mode
        self.player_name = player_name
        self.map_name = map_name
        self.map_data = get_map(map_name)
        self.walls = self.map_data["walls"]
        self.tick_count = 0
        self.game_over = False
        self.winner = None
        self.enabled_ai_ids = enabled_ai_ids if enabled_ai_ids is not None else []

        self.total_food_eaten = 0
        self.golden_food = None
        self.golden_timer = 0

        self.on_eat = None
        self.on_golden_eat = None
        self.on_death = None
        self.on_level_up = None

        print(f"[Map] {self.map_name} loaded, {len(self.walls)} walls, enabled AI: {self.enabled_ai_ids}")

        self._init_snakes()
        self.food = self._spawn_food()

    # ------------------------------------------------------------------
    def _init_snakes(self):
        self.snakes = {}
        configs = []

        # Player snake (if pvai mode)
        if self.mode == "pvai":
            configs.append((PLAYER_ID, (5, GRID_ROWS//2), RIGHT, self.player_name))

        # Add only enabled AI snakes
        if ASTAR_ID in self.enabled_ai_ids:
            configs.append((ASTAR_ID, (GRID_COLS-6, GRID_ROWS//2-4), LEFT, None))
        if GREEDY_ID in self.enabled_ai_ids:
            configs.append((GREEDY_ID, (GRID_COLS//2, GRID_ROWS-5), UP, None))
        if MINIMAX_ID in self.enabled_ai_ids:
            configs.append((MINIMAX_ID, (5, 5), RIGHT, None))

        for item in configs:
            if len(item) == 4:
                sid, start_pos, direction, custom_name = item
            else:
                sid, start_pos, direction = item
                custom_name = None

            # Wall avoidance
            if start_pos in self.walls:
                found = False
                for radius in range(1, 5):
                    for dx in range(-radius, radius+1):
                        for dy in range(-radius, radius+1):
                            new_pos = (start_pos[0] + dx, start_pos[1] + dy)
                            if (0 <= new_pos[0] < GRID_COLS and 0 <= new_pos[1] < GRID_ROWS
                                and new_pos not in self.walls):
                                start_pos = new_pos
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break

            if custom_name:
                self.snakes[sid] = Snake(sid, start_pos=start_pos, start_dir=direction, length=3, custom_name=custom_name)
            else:
                self.snakes[sid] = Snake(sid, start_pos=start_pos, start_dir=direction, length=3)

    # ------------------------------------------------------------------
    # Spawn food (unchanged)
    # ------------------------------------------------------------------
    def _spawn_food(self, avoid=None):
        if avoid is None:
            avoid = set()
        occupied = self._all_cells().union(self.walls).union(avoid)
        if self.golden_food:
            occupied.add(self.golden_food)
        free_cells = [(x,y) for x in range(GRID_COLS) for y in range(GRID_ROWS) if (x,y) not in occupied]
        if free_cells:
            return random.choice(free_cells)
        return None

    def _spawn_golden_food(self):
        occupied = self._all_cells().union(self.walls)
        if self.food:
            occupied.add(self.food)
        free_cells = [(x,y) for x in range(GRID_COLS) for y in range(GRID_ROWS) if (x,y) not in occupied]
        if free_cells:
            return random.choice(free_cells)
        return None

    # ------------------------------------------------------------------
    # Game tick (unchanged)
    # ------------------------------------------------------------------
    def tick(self, directions):
        if self.game_over:
            return

        self.tick_count += 1

        if self.golden_food is not None:
            self.golden_timer -= 1
            if self.golden_timer <= 0:
                self.golden_food = None
                if self.food is None:
                    self.food = self._spawn_food()

        for sid, snake in self.snakes.items():
            if snake.alive and sid in directions:
                snake.set_direction(directions[sid])
            if snake.alive:
                snake.commit_direction()

        new_heads = {}
        for sid, snake in self.snakes.items():
            if snake.alive:
                new_heads[sid] = snake.move()

        self._resolve_collisions(new_heads)

        # Normal food
        if self.food is not None:
            for sid, snake in self.snakes.items():
                if snake.alive and snake.head == self.food:
                    snake.grow()
                    if self.on_eat:
                        fx, fy = self.food
                        self.on_eat(fx * 22 + 11, fy * 22 + 11)
                    self.total_food_eaten += 1
                    if self.golden_food is None:
                        self.food = self._spawn_food()
                    else:
                        self.food = None
                    break

        # Golden food
        if self.golden_food is not None:
            for sid, snake in self.snakes.items():
                if snake.alive and snake.head == self.golden_food:
                    for _ in range(GOLDEN_SCORE_MULTIPLIER):
                        snake.grow()
                    if self.on_golden_eat:
                        fx, fy = self.golden_food
                        self.on_golden_eat(fx * 22 + 11, fy * 22 + 11)
                    self.golden_food = None
                    self.golden_timer = 0
                    self.food = self._spawn_food()
                    break

        # Spawn golden
        if (GOLDEN_FOOD_ENABLED and self.golden_food is None and
            self.total_food_eaten >= FOOD_COUNT_FOR_GOLDEN):
            self.golden_food = self._spawn_golden_food()
            if self.golden_food:
                self.golden_timer = GOLDEN_DURATION_FRAMES
                self.total_food_eaten = 0
                self.food = None

        self._check_game_over()

    # ------------------------------------------------------------------
    # Collision (unchanged)
    # ------------------------------------------------------------------
    def _resolve_collisions(self, new_heads):
        dead = set()
        all_bodies = {}
        for sid, snake in self.snakes.items():
            if snake.alive:
                all_bodies[sid] = set(snake.body)
        for sid, snake in self.snakes.items():
            if not snake.alive:
                continue
            head = snake.head
            hx, hy = head

            if not (0 <= hx < GRID_COLS and 0 <= hy < GRID_ROWS) or (head in self.walls):
                dead.add(sid)
                if self.on_death:
                    self.on_death(hx*22+11, hy*22+11)
                continue

            if head in list(snake.body)[1:]:
                dead.add(sid)
                if self.on_death:
                    self.on_death(hx*22+11, hy*22+11)
                continue

            for other_id, other_body_set in all_bodies.items():
                if other_id == sid:
                    continue
                if head in other_body_set:
                    dead.add(sid)
                    if self.on_death:
                        self.on_death(hx*22+11, hy*22+11)
                    break

        for sid in dead:
            self.snakes[sid].kill()

    def _check_game_over(self):
        alive = [sid for sid, s in self.snakes.items() if s.alive]
        if self.mode == "pvai":
            if PLAYER_ID not in alive:
                self.game_over = True
                self.winner = max(alive, key=lambda sid: self.snakes[sid].score) if alive else None
            elif len(alive) == 1 and alive[0] == PLAYER_ID:
                self.game_over = True
                self.winner = PLAYER_ID
        elif self.mode == "aibattle":
            if len(alive) <= 1:
                self.game_over = True
                self.winner = alive[0] if alive else None

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def _all_cells(self):
        cells = set(self.walls)
        for snake in self.snakes.values():
            cells.update(snake.cells)
        return cells

    def get_grid(self):
        grid = [[self.EMPTY] * GRID_COLS for _ in range(GRID_ROWS)]
        if self.food:
            fx, fy = self.food
            grid[fy][fx] = self.FOOD
        if self.golden_food:
            gx, gy = self.golden_food
            grid[gy][gx] = self.GOLDEN_FOOD
        for sid, snake in self.snakes.items():
            for (bx, by) in snake.body:
                grid[by][bx] = sid + 2
        return grid

    def get_obstacles(self, exclude_id=None):
        obstacles = set(self.walls)
        for sid, snake in self.snakes.items():
            if not snake.alive:
                continue
            cells = list(snake.body)
            if sid == exclude_id:
                obstacles.update(cells[1:])
            else:
                obstacles.update(cells)
        return obstacles

    def alive_snakes(self):
        return {sid: s for sid, s in self.snakes.items() if s.alive}

    def scores(self):
        return {sid: s.score for sid, s in self.snakes.items()}
    
    