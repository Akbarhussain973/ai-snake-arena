# ui.py
import pygame
import random
from constants import (
    BG_COLOR, GRID_COLOR, PANEL_BG, PANEL_BORDER, ACCENT,
    TEXT_PRIMARY, TEXT_SECONDARY, WHITE, BLACK,
    GRID_WIDTH, GRID_HEIGHT, PANEL_WIDTH, WINDOW_HEIGHT,
    CELL_SIZE, SNAKE_ALGO, GOLDEN_COLOR
)

class GameUI:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self._diff_flash_timer = 0
        self.particles = []
        self.flash_alpha = 0
        self.shake_amount = 0
        self.game_over = False

    def set_game_over(self):
        self.game_over = True
        self.shake_amount = 0
        self.flash_alpha = 0
        self.particles.clear()

    def trigger_diff_flash(self):
        self._diff_flash_timer = 45

    def add_levelup_flash(self):
        if not self.game_over:
            self.flash_alpha = 200

    def add_screen_shake(self, amount=8):
        if not self.game_over:
            self.shake_amount = min(20, self.shake_amount + amount)

    # --- Particles ---
    def add_eat_particles(self, x, y):
        if self.game_over:
            return
        for _ in range(15):
            self.particles.append({
                'x': x, 'y': y,
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'life': 30,
                'color': (255, 255, 100)
            })

    def add_golden_particles(self, x, y):
        if self.game_over:
            return
        self.add_screen_shake(10)
        for _ in range(30):
            self.particles.append({
                'x': x, 'y': y,
                'dx': random.uniform(-5, 5),
                'dy': random.uniform(-5, 5),
                'life': 40,
                'color': (255, 215, 0)
            })

    def add_death_particles(self, x, y):
        if self.game_over:
            return
        self.add_screen_shake(12)
        for _ in range(40):
            self.particles.append({
                'x': x, 'y': y,
                'dx': random.uniform(-6, 6),
                'dy': random.uniform(-6, 6),
                'life': 45,
                'color': (255, 50, 50)
            })

    def update_particles(self):
        for p in self.particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)

    def draw_particles(self):
        for p in self.particles:
            surf = pygame.Surface((6,6), pygame.SRCALPHA)
            intensity = min(255, int(255 * p['life'] / 30))
            color = (p['color'][0], p['color'][1], p['color'][2], intensity)
            pygame.draw.circle(surf, color, (3,3), 3)
            self.screen.blit(surf, (int(p['x']-3), int(p['y']-3)))

    # --- Main draw ---
    def draw(self, game, difficulty_manager):
        game_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        game_surface.fill(BG_COLOR)
        self._draw_grid(game_surface)
        self._draw_walls(game_surface, game.walls)
        if game.food is not None:
            self._draw_food(game_surface, game.food)
        if game.golden_food is not None:
            self._draw_golden_food(game_surface, game.golden_food)
        for snake in game.snakes.values():
            if snake.alive:
                self._draw_snake(game_surface, snake)

        if not self.game_over and self.shake_amount > 0:
            off_x = random.randint(-self.shake_amount, self.shake_amount)
            off_y = random.randint(-self.shake_amount, self.shake_amount)
            self.screen.blit(game_surface, (off_x, off_y))
            self.shake_amount = max(0, self.shake_amount - 3)
        else:
            self.screen.blit(game_surface, (0, 0))

        if not self.game_over:
            self.update_particles()
            self.draw_particles()
            if self.flash_alpha > 0:
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, self.flash_alpha))
                self.screen.blit(overlay, (0, 0))
                self.flash_alpha = max(0, self.flash_alpha - 15)

        self._draw_panel(self.screen, game, difficulty_manager)

    # --- Drawing helpers ---
    def _draw_grid(self, surface):
        for x in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x,0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0,y), (GRID_WIDTH, y))

    def _draw_walls(self, surface, walls):
        for wx, wy in walls:
            rect = pygame.Rect(wx * CELL_SIZE, wy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, (60, 60, 80), rect)
            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(surface, (80, 80, 100), inner_rect, border_radius=2)
            pygame.draw.line(surface, (110, 110, 130), (rect.left, rect.top), (rect.right-1, rect.top), 1)
            pygame.draw.line(surface, (110, 110, 130), (rect.left, rect.top), (rect.left, rect.bottom-1), 1)
            pygame.draw.line(surface, (40, 40, 55), (rect.left+1, rect.bottom-1), (rect.right-1, rect.bottom-1), 1)
            pygame.draw.line(surface, (40, 40, 55), (rect.right-1, rect.top+1), (rect.right-1, rect.bottom-1), 1)
            pygame.draw.rect(surface, (140, 140, 160), rect, 1)

    def _draw_food(self, surface, food_pos):
        fx, fy = food_pos
        cx = fx * CELL_SIZE + CELL_SIZE // 2
        cy = fy * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 3
        pygame.draw.circle(surface, WHITE, (cx, cy), radius)
        pygame.draw.circle(surface, (200,200,255), (cx, cy), radius+2, 1)

    def _draw_golden_food(self, surface, pos):
        fx, fy = pos
        cx = fx * CELL_SIZE + CELL_SIZE // 2
        cy = fy * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(surface, GOLDEN_COLOR, (cx, cy), radius+3)
        pygame.draw.circle(surface, (255, 255, 200), (cx, cy), radius+1)
        pygame.draw.circle(surface, (255, 220, 100), (cx, cy), radius)

    def _draw_snake(self, surface, snake):
        for i, (bx, by) in enumerate(snake.body):
            rect = pygame.Rect(bx*CELL_SIZE+1, by*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)
            color = snake.color_head if i == 0 else snake.color_body
            pygame.draw.rect(surface, color, rect, border_radius=4)
            if i == 0:
                pygame.draw.rect(surface, (255,255,255,80), rect, 1, border_radius=4)
        self._draw_eyes(surface, snake.head, snake.direction)

    def _draw_eyes(self, surface, head_pos, direction):
        bx, by = head_pos
        cx = bx * CELL_SIZE + CELL_SIZE // 2
        cy = by * CELL_SIZE + CELL_SIZE // 2
        dx, dy = direction
        if dx != 0:
            eye1 = (cx + dx*4, cy - 4)
            eye2 = (cx + dx*4, cy + 4)
        else:
            eye1 = (cx - 4, cy + dy*4)
            eye2 = (cx + 4, cy + dy*4)
        for eye in (eye1, eye2):
            pygame.draw.circle(surface, WHITE, eye, 3)
            pygame.draw.circle(surface, BLACK, eye, 1)

    # --- Side panel (updated to show player name) ---
    def _draw_panel(self, screen, game, difficulty_manager):
        px = GRID_WIDTH
        pygame.draw.rect(screen, PANEL_BG, (px, 0, PANEL_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(screen, PANEL_BORDER, (px,0), (px, WINDOW_HEIGHT), 2)
        y = 20
        title = self.fonts["heading"].render("SNAKE ARENA", True, ACCENT)
        screen.blit(title, (px+20, y))
        y += 40

        # Display player name if in pvai mode and name exists
        if game.mode == "pvai" and hasattr(game, 'player_name'):
            name_text = f"Player: {game.player_name}"
            name_surf = self.fonts["small"].render(name_text, True, ACCENT)
            screen.blit(name_surf, (px+20, y))
            y += 25

        pygame.draw.line(screen, PANEL_BORDER, (px+10,y), (px+PANEL_WIDTH-10,y))
        y += 15
        for sid, snake in game.snakes.items():
            y = self._draw_snake_card(screen, snake, px, y, game.mode)
            y += 10
        pygame.draw.line(screen, PANEL_BORDER, (px+10,y), (px+PANEL_WIDTH-10,y))
        y += 15
        self._draw_difficulty_badge(screen, difficulty_manager, px, y)
        y += 70
        if game.mode == "pvai":
            self._draw_controls_hint(screen, px, WINDOW_HEIGHT-70)

    def _draw_snake_card(self, screen, snake, px, y, mode):
        color = snake.color_head if snake.alive else TEXT_SECONDARY
        dot_x = px+20
        pygame.draw.circle(screen, color, (dot_x, y+10), 7)
        name_surf = self.fonts["body"].render(snake.name, True, TEXT_PRIMARY if snake.alive else TEXT_SECONDARY)
        screen.blit(name_surf, (dot_x+16, y))
        algo_surf = self.fonts["small"].render(SNAKE_ALGO[snake.id], True, TEXT_SECONDARY)
        screen.blit(algo_surf, (dot_x+16, y+20))
        score_str = str(snake.score)
        score_surf = self.fonts["score"].render(score_str, True, color)
        score_x = px+PANEL_WIDTH-20-score_surf.get_width()
        screen.blit(score_surf, (score_x, y))
        if not snake.alive:
            dead_surf = self.fonts["small"].render("✕ eliminated", True, (180,60,60))
            screen.blit(dead_surf, (dot_x+16, y+36))
        return y+55

    def _draw_difficulty_badge(self, screen, difficulty_manager, px, y):
        label = difficulty_manager.get_label()
        color = difficulty_manager.get_color()
        if self._diff_flash_timer > 0:
            self._diff_flash_timer -= 1
            if self._diff_flash_timer % 8 < 4:
                color = WHITE
        title_surf = self.fonts["small"].render("DIFFICULTY", True, TEXT_SECONDARY)
        screen.blit(title_surf, (px+20, y))
        badge_rect = pygame.Rect(px+20, y+18, PANEL_WIDTH-40, 32)
        pygame.draw.rect(screen, color, badge_rect, border_radius=6)
        label_surf = self.fonts["heading"].render(label, True, BLACK)
        lx = badge_rect.centerx - label_surf.get_width()//2
        ly = badge_rect.centery - label_surf.get_height()//2
        screen.blit(label_surf, (lx, ly))

    def _draw_controls_hint(self, screen, px, y):
        lines = ["CONTROLS", "↑ ↓ ← →  or  W A S D"]
        screen.blit(self.fonts["small"].render(lines[0], True, TEXT_SECONDARY), (px+20, y))
        screen.blit(self.fonts["small"].render(lines[1], True, TEXT_SECONDARY), (px+20, y+18))

    def draw_pause(self):
        overlay = pygame.Surface((GRID_WIDTH, GRID_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,140))
        self.screen.blit(overlay, (0,0))
        txt = self.fonts["heading"].render("PAUSED — press P to resume", True, ACCENT)
        x = GRID_WIDTH//2 - txt.get_width()//2
        y = GRID_HEIGHT//2 - txt.get_height()//2
        self.screen.blit(txt, (x,y))
        
        