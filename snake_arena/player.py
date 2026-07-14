# player.py
# Translates Pygame key events into direction commands for the player snake.
# Uses a buffer to store the most recent valid direction until the game asks for it.

import pygame
from constants import UP, DOWN, LEFT, RIGHT

class PlayerInput:
    """
    Buffers keyboard input for the player snake.
    The game calls consume() once per tick to get the next direction.
    """

    # Mapping from Pygame key codes to direction vectors
    KEY_MAP = {
        pygame.K_UP:    UP,
        pygame.K_w:     UP,
        pygame.K_DOWN:  DOWN,
        pygame.K_s:     DOWN,
        pygame.K_LEFT:  LEFT,
        pygame.K_a:     LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_d:     RIGHT,
    }

    def __init__(self):
        self._buffered = None   # last direction pressed (may be None)

    def handle_event(self, event):
        """
        Call this for each pygame.KEYDOWN event in the main loop.
        Stores the direction if the key is one of the movement keys.
        """
        if event.type == pygame.KEYDOWN:
            direction = self.KEY_MAP.get(event.key)
            if direction is not None:
                self._buffered = direction

    def consume(self):
        """
        Returns the buffered direction and clears the buffer.
        Called once per game tick. Returns None if no key was pressed since last consume.
        """
        direction = self._buffered
        self._buffered = None
        return direction
    
    