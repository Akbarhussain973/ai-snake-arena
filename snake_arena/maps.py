# maps.py
from constants import GRID_COLS, GRID_ROWS

# Snake start positions for reference
START_POSITIONS = {
    "player": (5, GRID_ROWS // 2),          # (5, 15)
    "astar": (GRID_COLS - 6, GRID_ROWS // 2 - 4),  # (24, 11)
    "greedy": (GRID_COLS // 2, GRID_ROWS - 5),     # (15, 25)
    "minimax": (5, 5)                               # moved to corner
}

def safe_zone(radius=3):
    safe = set()
    for sx, sy in START_POSITIONS.values():
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                    safe.add((nx, ny))
    return safe

SAFE = safe_zone(3)

# ------------------------------------------------------------
# Open spiral – a single winding corridor, no closed loop
# ------------------------------------------------------------
def generate_open_spiral():
    walls = set()
    center_x, center_y = GRID_COLS // 2, GRID_ROWS // 2
    
    ring_sizes = [2, 4, 6, 8, 10]  # half-sizes of rings
    for r in ring_sizes:
        # Draw three walls of each ring (top, left, right) but leave bottom open
        # Top edge
        for x in range(center_x - r, center_x + r + 1):
            y = center_y - r
            if (x, y) not in SAFE and not (x == center_x and y == center_y - r):
                walls.add((x, y))
        # Left edge
        for y in range(center_y - r, center_y + r + 1):
            x = center_x - r
            if (x, y) not in SAFE and not (x == center_x - r and y == center_y):
                walls.add((x, y))
        # Right edge
        for y in range(center_y - r, center_y + r + 1):
            x = center_x + r
            if (x, y) not in SAFE and not (x == center_x + r and y == center_y):
                walls.add((x, y))
        # Bottom edge is left open to allow exit
    # Then add a few extra walls to make it look like a spiral
    return walls

# Alternative: a safe "spiral" that is actually a maze-like path
# I'll provide a simpler, guaranteed non-enclosing pattern: "swirl"
def generate_swirl():
    walls = set()
    # Draw a large "S" shape wall
    for x in range(5, 25):
        if x < 15:
            walls.add((x, 10))
        else:
            walls.add((x, 20))
    for y in range(10, 21):
        walls.add((5, y))
    for y in range(10, 21):
        walls.add((24, y))
    # Remove any walls that are in safe zone
    return {w for w in walls if w not in SAFE and w not in START_POSITIONS.values()}

MAPS = {
    "classic": {
        "name": "CLASSIC",
        "walls": set(),
        "description": "No walls – open arena"
    },
    "maze": {
        "name": "MAZE",
        "walls": {
            (x, y) for x in range(5, 26) for y in [10, 12, 14, 16, 18, 20]
            if (x, y) not in SAFE
        } | {
            (x, y) for x in [8, 12, 16, 20, 24] for y in range(5, 26)
            if (x, y) not in SAFE and y % 2 == 0
        },
        "description": "Zigzag maze with obstacles"
    },
    "cross": {
        "name": "CROSS",
        "walls": {
            (x, y) for x in range(8, 24) for y in [13, 14, 15, 16, 17]
            if (x, y) not in SAFE
        } | {
            (x, y) for x in [13, 14, 15, 16, 17] for y in range(8, 24)
            if (x, y) not in SAFE
        },
        "description": "A thick cross (+) pattern"
    },
    "spiral": {
        "name": "SPIRAL",
        "walls": generate_swirl(),   # Using swirl instead of enclosed spiral
        "description": "A winding S‑shaped corridor (open, no traps)"
    }
}

DEFAULT_MAP = "classic"

def get_map(map_name):
    return MAPS.get(map_name, MAPS[DEFAULT_MAP])

def get_map_names():
    return list(MAPS.keys())
