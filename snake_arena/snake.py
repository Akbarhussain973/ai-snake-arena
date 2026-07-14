# snake.py
# Shared Snake class – used by Player, A* Snake, and Greedy Snake.
# Handles body (deque), movement, growing, collision flags, and direction buffering.
# All snakes are equal; only the decision-maker differs.

from collections import deque
from constants import OPPOSITE, SNAKE_HEAD_COLORS, SNAKE_BODY_COLORS, SNAKE_NAMES

class Snake:
    """
    Represents a single snake on the board.
    Direction changes are buffered to avoid 180° reversals within the same tick.
    The 'grew' flag allows the snake to extend after eating food.
    """

    def __init__(self, snake_id: int, start_pos: tuple, start_dir: tuple, length: int = 3,
                 custom_name: str = None, custom_head_color: tuple = None, custom_body_color: tuple = None):
        """
        snake_id   : PLAYER_ID, ASTAR_ID, GREEDY_ID (or any integer for dummy snakes)
        start_pos  : (x, y) grid coordinates for the head
        start_dir  : direction tuple (dx, dy)
        length     : initial body length (including head)
        custom_name: optional name override (for dummy snakes)
        custom_head_color, custom_body_color: optional color overrides
        """
        self.id = snake_id
        
        # Name: use custom_name if provided, else lookup in SNAKE_NAMES, else fallback
        if custom_name is not None:
            self.name = custom_name
        else:
            self.name = SNAKE_NAMES.get(snake_id, f"Snake_{snake_id}")
        
        # Head color
        if custom_head_color is not None:
            self.color_head = custom_head_color
        else:
            self.color_head = SNAKE_HEAD_COLORS.get(snake_id, (128, 128, 128))
        
        # Body color
        if custom_body_color is not None:
            self.color_body = custom_body_color
        else:
            self.color_body = SNAKE_BODY_COLORS.get(snake_id, (100, 100, 100))

        # Build initial body from head backwards
        x, y = start_pos
        dx, dy = start_dir
        self.body = deque()
        for i in range(length):
            self.body.append((x - dx * i, y - dy * i))

        self.direction = start_dir      # current moving direction
        self._next_dir = start_dir      # buffered direction for next move
        self.score = 0
        self.alive = True
        self.grew = False               # if True, do not remove tail on next move

    # ------------------------------------------------------------------
    #  Direction handling
    # ------------------------------------------------------------------
    def set_direction(self, new_dir: tuple):
        """
        Buffer a direction change. Prevents 180° instant reversal.
        Actual change happens at commit_direction() just before move.
        """
        if new_dir != OPPOSITE.get(self.direction):
            self._next_dir = new_dir

    def commit_direction(self):
        """Apply the buffered direction. Called once per game tick."""
        self.direction = self._next_dir

    # ------------------------------------------------------------------
    #  Movement & growth
    # ------------------------------------------------------------------
    def move(self) -> tuple:
        """
        Move the snake one step in the current direction.
        Returns the new head position.
        If grew flag is True, the tail stays (snake lengthens).
        Otherwise, pop the tail (normal movement).
        """
        hx, hy = self.head
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)

        self.body.appendleft(new_head)

        if self.grew:
            self.grew = False       # consume the growth flag
        else:
            self.body.pop()          # remove tail

        return new_head

    def grow(self):
        """Called when snake eats food. Next move will lengthen the snake."""
        self.grew = True
        self.score += 1

    def kill(self):
        """Mark snake as dead. It will be removed from the game."""
        self.alive = False

    # ------------------------------------------------------------------
    #  Properties
    # ------------------------------------------------------------------
    @property
    def head(self) -> tuple:
        """Return current head position."""
        return self.body[0]

    @property
    def cells(self) -> set:
        """Return a set of all occupied cells (for fast collision checks)."""
        return set(self.body)

    def occupies(self, pos: tuple) -> bool:
        """Check if the snake occupies a specific cell."""
        return pos in self.body

    def __repr__(self):
        return f"<Snake id={self.id} name={self.name} head={self.head} score={self.score} alive={self.alive}>"
    
    