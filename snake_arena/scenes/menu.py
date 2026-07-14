# scenes/menu.py 
import pygame
import random
import math
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_COLS, GRID_ROWS, CELL_SIZE,
    BG_COLOR, ACCENT, TEXT_SECONDARY, TEXT_PRIMARY, RIGHT
)
from snake import Snake
from ai_greedy import GreedyAI

class MenuScene:
    def __init__(self):
        self.snake = Snake(
            snake_id=99,
            start_pos=(GRID_COLS // 2, GRID_ROWS // 2),
            start_dir=RIGHT,
            length=6,
            custom_name="MenuSnake",
            custom_head_color=(0, 200, 200),
            custom_body_color=(200, 100, 0)
        )
        self.ai = GreedyAI(99)
        self.frame_counter = 0
        self.fake_food = (GRID_COLS // 2 + 5, GRID_ROWS // 2)
        self.hue = 0
        self.button_pulse = 0.0
        self.particles = []
        for _ in range(80):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'size': random.randint(2, 6),
                'speed': random.uniform(0.5, 2.0),
                'color': [random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)]
            })

    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        selected = 0
        button_rects = []
        grid_surface = pygame.Surface((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))

        while True:
            self.frame_counter += 1
            self.hue = (self.hue + 0.5) % 360
            self.button_pulse = (self.button_pulse + 0.05) % (2 * math.pi)

            if self.frame_counter % 8 == 0:
                self._move_background_snake()

            for p in self.particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = WINDOW_HEIGHT
                    p['x'] = random.randint(0, WINDOW_WIDTH)
                    p['color'] = [random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % 3
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if selected == 0:
                            return "mode_select"
                        elif selected == 1:
                            return "high_scores"
                        else:
                            return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return "mode_select"
                            elif i == 1:
                                return "high_scores"
                            else:
                                return "quit"

            # Gradient background
            for y in range(WINDOW_HEIGHT):
                ratio = y / WINDOW_HEIGHT
                r = int(18 + 10 * ratio)
                g = int(18 + 5 * ratio)
                b = int(30 + 20 * ratio)
                pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

            self._draw_background(grid_surface)
            screen.blit(grid_surface, (0, 0))

            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            # Rainbow title
            title_font = fonts["title"]
            title_text = "SNAKE ARENA"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (self.hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 100))
                start_x += char_surf.get_width()

            # Subtitle fade
            sub_font = fonts["body"]
            alpha = int(150 + 105 * (0.5 + 0.5 * math.sin(self.frame_counter * 0.02)))
            sub_surf = sub_font.render("AI Battle Royale", True, (200, 200, 200))
            sub_surf.set_alpha(alpha)
            sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH//2, 170))
            screen.blit(sub_surf, sub_rect)

            # Buttons
            button_rects = []
            btn_y = 260
            labels = ["PLAY", "HIGH SCORES", "QUIT"]
            for i, label in enumerate(labels):
                scale = 1 + 0.05 * math.sin(self.button_pulse) if i == selected else 1.0
                if i == selected:
                    btn_color = pygame.Color(0)
                    btn_color.hsla = ((self.hue + i * 30) % 360, 100, 60, 100)
                else:
                    btn_color = TEXT_SECONDARY

                surf = fonts["heading"].render(label, True, btn_color)
                if scale != 1.0:
                    w, h = surf.get_size()
                    scaled = pygame.transform.scale(surf, (int(w * scale), int(h * scale)))
                    rect = scaled.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*60))
                else:
                    rect = surf.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*60))

                glow_rect = rect.inflate(60, 30)
                glow_color = (btn_color.r, btn_color.g, btn_color.b) if i == selected else (40,40,40)
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=15, width=2 if i==selected else 1)

                if scale != 1.0:
                    screen.blit(scaled, rect)
                else:
                    screen.blit(surf, rect)
                button_rects.append(glow_rect)

            # Particles
            for p in self.particles:
                psurf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(psurf, (p['color'][0], p['color'][1], p['color'][2], 180), (p['size'], p['size']), p['size'])
                screen.blit(psurf, (int(p['x'] - p['size']), int(p['y'] - p['size'])))

            # Instructions
            inst = fonts["small"].render("↑ ↓  ENTER  |  ESC to quit", True, TEXT_SECONDARY)
            inst_rect = inst.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 40))
            screen.blit(inst, inst_rect)

            pygame.display.flip()
            clock.tick(30)

    def _move_background_snake(self):
        obstacles = set()
        for x in range(GRID_COLS):
            obstacles.add((x, 0))
            obstacles.add((x, GRID_ROWS - 1))
        for y in range(GRID_ROWS):
            obstacles.add((0, y))
            obstacles.add((GRID_COLS - 1, y))
        for i, cell in enumerate(self.snake.body):
            if i != 0:
                obstacles.add(cell)
        if self.frame_counter % 60 == 0:
            self.fake_food = (random.randint(5, GRID_COLS-6), random.randint(5, GRID_ROWS-6))
        head = self.snake.head
        direction = self.ai.get_direction(head, self.fake_food, obstacles, [], self.snake.direction)
        self.snake.set_direction(direction)
        self.snake.commit_direction()
        self.snake.move()
        if head in obstacles:
            self.snake = Snake(99, (GRID_COLS//2, GRID_ROWS//2), RIGHT, 6,
                               custom_name="MenuSnake", custom_head_color=(0,200,200), custom_body_color=(200,100,0))
            self.fake_food = (GRID_COLS//2+5, GRID_ROWS//2)

    def _draw_background(self, surface):
        surface.fill((0,0,0))
        grid_color = (60, 60, 70)
        for x in range(0, GRID_COLS*CELL_SIZE, CELL_SIZE):
            pygame.draw.line(surface, grid_color, (x,0), (x, GRID_ROWS*CELL_SIZE))
        for y in range(0, GRID_ROWS*CELL_SIZE, CELL_SIZE):
            pygame.draw.line(surface, grid_color, (0,y), (GRID_COLS*CELL_SIZE, y))
        for i, (bx, by) in enumerate(self.snake.body):
            rect = pygame.Rect(bx*CELL_SIZE+1, by*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)
            if i == 0:
                color = self.snake.color_head
                pygame.draw.rect(surface, (100,255,255), rect.inflate(4,4), border_radius=6)
            else:
                intensity = max(80, 200 - i*10)
                color = (200, intensity//2, 0)
            pygame.draw.rect(surface, color, rect, border_radius=4)
        fx, fy = self.fake_food
        cx = fx*CELL_SIZE + CELL_SIZE//2
        cy = fy*CELL_SIZE + CELL_SIZE//2
        pulse = (self.frame_counter % 20) / 20.0
        radius = int(3 + pulse * 2)
        pygame.draw.circle(surface, (255, 100, 100), (cx, cy), radius)