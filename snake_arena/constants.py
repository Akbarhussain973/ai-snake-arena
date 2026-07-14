# constants.py
# Central configuration for Snake Arena.

import pygame

# ------------------------------
#  Window & Grid
# ------------------------------
WINDOW_TITLE = "Snake Arena"
GRID_COLS = 30
GRID_ROWS = 30
CELL_SIZE = 22
PANEL_WIDTH = 240

GRID_WIDTH = GRID_COLS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE
WINDOW_WIDTH = GRID_WIDTH + PANEL_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

FPS_BASE = 12

# Difficulty presets for explicit mode selection
DIFFICULTY_PRESETS = {
    "easy": {
        "name": "EASY",
        "base_speed": 8,
        "ai_difficulty": 0,
        "ai_aggression": 0,
        "adaptive_enabled": False
    },
    "medium": {
        "name": "MEDIUM",
        "base_speed": 12,
        "ai_difficulty": 1,
        "ai_aggression": 1,
        "adaptive_enabled": False
    },
    "hard": {
        "name": "HARD",
        "base_speed": 16,
        "ai_difficulty": 2,
        "ai_aggression": 2,
        "adaptive_enabled": False
    }
}

# Adaptive difficulty thresholds (when enabled)
ADAPTIVE_THRESHOLDS = [5, 15]           # score >=5 -> Medium, >=15 -> Hard

# Golden food settings
GOLDEN_FOOD_ENABLED = True
FOOD_COUNT_FOR_GOLDEN = 5               # after 5 normal foods
GOLDEN_SCORE_MULTIPLIER = 10
GOLDEN_DURATION_FRAMES = 150            # ~5 sec at 30 FPS
GOLDEN_COLOR = (255, 215, 0)

# ------------------------------
#  Colors – Clean Modern Theme
# ------------------------------
BG_COLOR        = (18, 18, 18)
GRID_COLOR      = (28, 28, 28)
PANEL_BG        = (24, 24, 24)
PANEL_BORDER    = (40, 40, 40)
ACCENT          = (99, 202, 183)
ACCENT_DIM      = (60, 130, 118)

PLAYER_HEAD     = (72, 149, 239)
PLAYER_BODY     = (50, 110, 185)
ASTAR_HEAD      = (239, 83, 80)
ASTAR_BODY      = (180, 55, 55)
GREEDY_HEAD     = (255, 202, 58)
GREEDY_BODY     = (195, 150, 30)
MINIMAX_HEAD    = (156, 39, 176)          # purple
MINIMAX_BODY    = (123, 31, 162)          # dark purple

MENU_SNAKE      = (55, 55, 55)
FOOD_COLOR      = (255, 255, 255)
FOOD_GLOW       = (200, 200, 200)
TEXT_PRIMARY    = (240, 240, 240)
TEXT_SECONDARY  = (120, 120, 120)
TEXT_ACCENT     = ACCENT

COLOR_EASY      = (99, 202, 120)
COLOR_MEDIUM    = (255, 202, 58)
COLOR_HARD      = (239, 83, 80)

WHITE           = (255, 255, 255)
BLACK           = (0, 0, 0)

# ------------------------------
#  Directions
# ------------------------------
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)
ALL_DIRS = [UP, DOWN, LEFT, RIGHT]

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

# ------------------------------
#  Snake IDs & Metadata
# ------------------------------
PLAYER_ID = 0
ASTAR_ID  = 1
GREEDY_ID = 2
MINIMAX_ID = 3

SNAKE_NAMES = {
    PLAYER_ID: "Player",
    ASTAR_ID:  "A* Snake",
    GREEDY_ID: "Greedy Snake",
    MINIMAX_ID: "Minimax Snake",
}
SNAKE_ALGO = {
    PLAYER_ID: "Keyboard",
    ASTAR_ID:  "A* Pathfinding",
    GREEDY_ID: "Greedy Best-First",
    MINIMAX_ID: "Minimax + Alpha-Beta",
}
SNAKE_HEAD_COLORS = {
    PLAYER_ID: PLAYER_HEAD,
    ASTAR_ID:  ASTAR_HEAD,
    GREEDY_ID: GREEDY_HEAD,
    MINIMAX_ID: MINIMAX_HEAD,
}
SNAKE_BODY_COLORS = {
    PLAYER_ID: PLAYER_BODY,
    ASTAR_ID:  ASTAR_BODY,
    GREEDY_ID: GREEDY_BODY,
    MINIMAX_ID: MINIMAX_BODY,
}

# ------------------------------
#  Difficulty Labels & Colors
# ------------------------------
DIFF_LABELS = {0: "EASY", 1: "MEDIUM", 2: "HARD"}
DIFF_COLORS = {0: COLOR_EASY, 1: COLOR_MEDIUM, 2: COLOR_HARD}

# ------------------------------
#  Fonts
# ------------------------------
def load_fonts():
    fonts = {}
    try:
        fonts["title"]   = pygame.font.SysFont("segoeui", 52, bold=True)
        fonts["heading"] = pygame.font.SysFont("segoeui", 22, bold=True)
        fonts["body"]    = pygame.font.SysFont("segoeui", 17)
        fonts["small"]   = pygame.font.SysFont("segoeui", 13)
        fonts["score"]   = pygame.font.SysFont("couriernew", 28, bold=True)
        fonts["big"]     = pygame.font.SysFont("segoeui", 72, bold=True)
    except:
        default = pygame.font.SysFont(None, 24)
        fonts = {k: default for k in ["title","heading","body","small","score","big"]}
    return fonts

