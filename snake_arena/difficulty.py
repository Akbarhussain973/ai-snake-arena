# difficulty.py
# Handles both explicit difficulty (Easy/Medium/Hard) and adaptive difficulty (based on player score).

from constants import DIFFICULTY_PRESETS, ADAPTIVE_THRESHOLDS, DIFF_LABELS, DIFF_COLORS

class DifficultyManager:
    def __init__(self, mode="pvai", explicit_difficulty="medium", adaptive=False, custom_fps=None):
        """
        mode: "pvai" or "aibattle"
        explicit_difficulty: "easy", "medium", or "hard" (used if adaptive=False)
        adaptive: if True, difficulty changes based on player score
        custom_fps: if provided, overrides the FPS from difficulty preset
        """
        self.mode = mode
        self.adaptive = adaptive
        self.explicit_level = explicit_difficulty
        self._current_level = explicit_difficulty
        self.player_score = 0
        self.custom_fps = custom_fps

    def update(self, player_score):
        """Called every tick to possibly adapt difficulty (if adaptive mode)."""
        self.player_score = player_score
        if not self.adaptive or self.mode != "pvai":
            return

        # Determine new level from thresholds
        new_level = "easy"
        if player_score >= ADAPTIVE_THRESHOLDS[1]:
            new_level = "hard"
        elif player_score >= ADAPTIVE_THRESHOLDS[0]:
            new_level = "medium"
        else:
            new_level = "easy"

        self._current_level = new_level

    def get_fps(self):
        """Return game speed (FPS) based on current difficulty, overridden by custom_fps if set."""
        if self.custom_fps is not None:
            return self.custom_fps
        if self.adaptive:
            level = self._current_level
        else:
            level = self.explicit_level
        return DIFFICULTY_PRESETS[level]["base_speed"]

    def get_label(self):
        if self.adaptive:
            return DIFF_LABELS[{"easy":0, "medium":1, "hard":2}[self._current_level]]
        else:
            return DIFFICULTY_PRESETS[self.explicit_level]["name"]

    def get_color(self):
        level = self._current_level if self.adaptive else self.explicit_level
        idx = {"easy":0, "medium":1, "hard":2}[level]
        return DIFF_COLORS[idx]

    def get_ai_difficulty(self):
        """Return AI difficulty level (0=easy,1=medium,2=hard)."""
        if self.adaptive:
            level = self._current_level
        else:
            level = self.explicit_level
        return DIFFICULTY_PRESETS[level]["ai_difficulty"]

    def get_ai_aggression(self):
        """Return aggression level (0,1,2) for greedy AI."""
        if self.adaptive:
            level = self._current_level
        else:
            level = self.explicit_level
        return DIFFICULTY_PRESETS[level]["ai_aggression"]

    def just_leveled_up(self, previous_level):
        # For adaptive, we compare numeric level; but we don't use this much.
        return False
    
    