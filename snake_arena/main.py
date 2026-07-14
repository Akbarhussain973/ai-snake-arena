# main.py (with speed slider)
import pygame
import sys
import json
import os
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    PLAYER_ID, ASTAR_ID, GREEDY_ID, MINIMAX_ID, load_fonts
)
from game import Game
from player import PlayerInput
from ai_astar import AStarAI
from ai_greedy import GreedyAI
from ai_minimax import MinimaxAI
from difficulty import DifficultyManager
from ui import GameUI
from sound_manager import SoundManager
from scenes.menu import MenuScene
from scenes.mode_select import ModeSelectScene
from scenes.game_over import GameOverScene
from scenes.high_scores import HighScoresScene
from scenes.difficulty_select import DifficultySelectScene
from scenes.map_select import MapSelectScene
from scenes.name_input import NameInputScene
from scenes.ai_select import AISelectScene
from scenes.speed_select import SpeedSelectScene

# ----------------------------------------------------------------------
# High Score Manager
# ----------------------------------------------------------------------
class HighScoreManager:
    def __init__(self, filename="high_scores.json"):
        self.filename = filename
        self.scores = {"pvai": [], "aibattle": []}
        self.load()
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    if "pvai" in data:
                        self.scores["pvai"] = data["pvai"]
                    if "aibattle" in data:
                        self.scores["aibattle"] = data["aibattle"]
            except:
                pass
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f, indent=2)
    def add_score(self, mode, name, score):
        if mode == "pvai":
            self.scores["pvai"].append({"name": name, "score": score})
            self.scores["pvai"].sort(key=lambda x: x["score"], reverse=True)
            self.scores["pvai"] = self.scores["pvai"][:5]
            self.save()
        elif mode == "aibattle":
            self.scores["aibattle"].append({"winner": name, "timestamp": pygame.time.get_ticks()})
            self.scores["aibattle"] = self.scores["aibattle"][-5:]
            self.save()
    def get_top_scores(self, mode):
        return self.scores.get(mode, [])

# ----------------------------------------------------------------------
# Main Game Loop
# ----------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    fonts = load_fonts()
    sounds = SoundManager()
    sounds.start_music()
    high_scores = HighScoreManager()

    current_scene = "menu"
    game_mode = "pvai"
    selected_difficulty = "medium"
    selected_speed = None
    selected_map = "classic"
    player_name = "Player"
    selected_ai_ids = [ASTAR_ID, GREEDY_ID]
    game = None
    player_input = None
    ai_brains = {}
    difficulty_mgr = None
    ui = None

    running = True
    while running:
        # ------------------------------ MENU ------------------------------
        if current_scene == "menu":
            scene = MenuScene()
            result = scene.run(screen, fonts)
            if result == "mode_select":
                current_scene = "mode_select"
            elif result == "high_scores":
                current_scene = "high_scores"
            else:
                running = False

        # ------------------------------ HIGH SCORES ------------------------------
        elif current_scene == "high_scores":
            scene = HighScoresScene()
            scene.run(screen, fonts)
            current_scene = "menu"

        # ------------------------------ MODE SELECT ------------------------------
        elif current_scene == "mode_select":
            scene = ModeSelectScene()
            result = scene.run(screen, fonts)
            if result in ("pvai", "aibattle"):
                game_mode = result
                if game_mode == "pvai":
                    current_scene = "name_input"
                else:
                    player_name = "AI Battle"
                    current_scene = "difficulty_select"
            elif result == "menu":
                current_scene = "menu"
            else:
                running = False

        # ------------------------------ NAME INPUT ------------------------------
        elif current_scene == "name_input":
            scene = NameInputScene()
            result = scene.run(screen, fonts)
            if result and result not in ("quit", "menu"):
                player_name = result
                current_scene = "difficulty_select"
            elif result == "menu":
                current_scene = "menu"
            elif result == "quit":
                running = False

        # ------------------------------ DIFFICULTY SELECT ------------------------------
        elif current_scene == "difficulty_select":
            scene = DifficultySelectScene()
            result = scene.run(screen, fonts)
            if result in ("easy", "medium", "hard"):
                selected_difficulty = result
                current_scene = "speed_select"
            elif result == "menu":
                current_scene = "menu"
            elif result == "quit":
                running = False

        # ------------------------------ SPEED SELECT ------------------------------
        elif current_scene == "speed_select":
            from constants import DIFFICULTY_PRESETS
            default_speed = DIFFICULTY_PRESETS[selected_difficulty]["base_speed"]
            scene = SpeedSelectScene()
            result = scene.run(screen, fonts, default_speed=default_speed)
            if isinstance(result, int):
                selected_speed = result
                current_scene = "map_select"
            elif result == "menu":
                current_scene = "menu"
            else:
                running = False

        # ------------------------------ MAP SELECT ------------------------------
        elif current_scene == "map_select":
            scene = MapSelectScene()
            result = scene.run(screen, fonts)
            if result in ("classic", "maze", "cross", "spiral"):
                selected_map = result
                current_scene = "ai_select"
            elif result == "menu":
                current_scene = "menu"
            elif result == "quit":
                running = False

        # ------------------------------ AI SELECT ------------------------------
        elif current_scene == "ai_select":
            scene = AISelectScene()
            result = scene.run(screen, fonts)
            if isinstance(result, list):
                selected_ai_ids = result
                game = Game(mode=game_mode, map_name=selected_map, player_name=player_name, enabled_ai_ids=selected_ai_ids)
                player_input = PlayerInput() if game_mode == "pvai" else None
                ai_brains = {}
                if ASTAR_ID in selected_ai_ids:
                    ai_brains[ASTAR_ID] = AStarAI(ASTAR_ID)
                if GREEDY_ID in selected_ai_ids:
                    ai_brains[GREEDY_ID] = GreedyAI(GREEDY_ID)
                if MINIMAX_ID in selected_ai_ids:
                    ai_brains[MINIMAX_ID] = MinimaxAI(MINIMAX_ID)
                difficulty_mgr = DifficultyManager(mode=game_mode,
                                                   explicit_difficulty=selected_difficulty,
                                                   adaptive=False,
                                                   custom_fps=selected_speed)
                ui = GameUI(screen, fonts)
                game.on_eat = ui.add_eat_particles
                game.on_golden_eat = ui.add_golden_particles
                game.on_death = ui.add_death_particles
                game.on_level_up = ui.add_levelup_flash
                current_scene = "game"
            elif result == "menu":
                current_scene = "menu"
            else:
                running = False

        # ------------------------------ GAME ------------------------------
        elif current_scene == "game":
            paused = False
            last_scores = game.scores()
            final_player_score = 0

            while not game.game_over and current_scene == "game":
                clock.tick(difficulty_mgr.get_fps())
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game.game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            game.game_over = True
                        if event.key == pygame.K_p:
                            paused = not paused
                        if player_input:
                            player_input.handle_event(event)
                if paused:
                    ui.draw_pause()
                    pygame.display.flip()
                    continue

                directions = {}
                if player_input:
                    dir_player = player_input.consume()
                    if dir_player:
                        directions[PLAYER_ID] = dir_player

                for sid, brain in ai_brains.items():
                    snake = game.snakes.get(sid)
                    if snake and snake.alive:
                        target = game.golden_food if game.golden_food is not None else game.food
                        if target is None:
                            target = snake.head
                        obstacles = game.get_obstacles(exclude_id=sid)
                        other_heads = [s.head for s in game.snakes.values() if s.alive and s.id != sid]
                        ai_diff = difficulty_mgr.get_ai_difficulty()
                        brain.set_difficulty(ai_diff)
                        direction = brain.get_direction(snake.head, target, obstacles,
                                                         other_heads, snake.direction)
                        directions[sid] = direction

                game.tick(directions)

                new_scores = game.scores()
                for sid, s in game.snakes.items():
                    if new_scores.get(sid, 0) > last_scores.get(sid, 0):
                        sounds.play("eat")
                    if not s.alive and last_scores.get(sid) is not None:
                        sounds.play("death")
                last_scores = new_scores.copy()

                if game_mode == "pvai" and game.snakes[PLAYER_ID].alive:
                    final_player_score = game.snakes[PLAYER_ID].score

                ui.draw(game, difficulty_mgr)
                pygame.display.flip()

            # Game over
            ui.set_game_over()
            winner_id = game.winner
            winner_name = game.snakes[winner_id].name if winner_id is not None else "Draw"
            scores_with_names = {}
            for snake in game.snakes.values():
                if snake.id == PLAYER_ID:
                    scores_with_names[player_name] = snake.score
                else:
                    scores_with_names[snake.name] = snake.score

            if game_mode == "pvai":
                high_scores.add_score("pvai", player_name, final_player_score)
            else:
                high_scores.add_score("aibattle", winner_name, 0)

            scene = GameOverScene()
            result = scene.run(screen, fonts, winner_name, scores_with_names, high_scores, game_mode)

            if result == "replay":
                game = Game(mode=game_mode, map_name=selected_map, player_name=player_name, enabled_ai_ids=selected_ai_ids)
                player_input = PlayerInput() if game_mode == "pvai" else None
                ai_brains = {}
                if ASTAR_ID in selected_ai_ids:
                    ai_brains[ASTAR_ID] = AStarAI(ASTAR_ID)
                if GREEDY_ID in selected_ai_ids:
                    ai_brains[GREEDY_ID] = GreedyAI(GREEDY_ID)
                if MINIMAX_ID in selected_ai_ids:
                    ai_brains[MINIMAX_ID] = MinimaxAI(MINIMAX_ID)
                difficulty_mgr = DifficultyManager(mode=game_mode,
                                                   explicit_difficulty=selected_difficulty,
                                                   adaptive=False,
                                                   custom_fps=selected_speed)
                ui = GameUI(screen, fonts)
                game.on_eat = ui.add_eat_particles
                game.on_golden_eat = ui.add_golden_particles
                game.on_death = ui.add_death_particles
                game.on_level_up = ui.add_levelup_flash
                current_scene = "game"
            elif result == "menu":
                current_scene = "menu"
            else:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    
    