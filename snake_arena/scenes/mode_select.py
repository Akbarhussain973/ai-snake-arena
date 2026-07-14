# scenes/mode_select.py (enhanced with animations)
import pygame
import random
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY

class ModeSelectScene:
    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        selected = 0
        button_rects = []
        hue = 0
        pulse = 0

        particles = []
        for _ in range(60):
            particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'size': random.randint(2, 5),
                'speed': random.uniform(0.5, 1.5),
                'color': [random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)]
            })

        while True:
            clock.tick(30)
            hue = (hue + 0.5) % 360
            pulse = (pulse + 0.05) % (2 * math.pi)

            for p in particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = WINDOW_HEIGHT
                    p['x'] = random.randint(0, WINDOW_WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % 2
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % 2
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return "pvai" if selected == 0 else "aibattle"
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            return "pvai" if i == 0 else "aibattle"

            # Gradient background
            for y in range(WINDOW_HEIGHT):
                ratio = y / WINDOW_HEIGHT
                r = int(18 + 10 * ratio)
                g = int(18 + 5 * ratio)
                b = int(30 + 20 * ratio)
                pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

            # Particles
            for p in particles:
                ps = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(ps, (p['color'][0], p['color'][1], p['color'][2], 160), (p['size'], p['size']), p['size'])
                screen.blit(ps, (int(p['x'] - p['size']), int(p['y'] - p['size'])))

            # Rainbow title
            title_font = fonts["title"]
            title_text = "SELECT MODE"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 100))
                start_x += char_surf.get_width()

            # Buttons
            button_rects = []
            btn_y = 280
            modes = ["Player vs AI", "AI Battle"]
            for i, label in enumerate(modes):
                scale = 1 + 0.05 * math.sin(pulse) if i == selected else 1.0
                if i == selected:
                    btn_color = pygame.Color(0)
                    btn_color.hsla = ((hue + i * 30) % 360, 100, 60, 100)
                else:
                    btn_color = TEXT_SECONDARY

                surf = fonts["heading"].render(label, True, btn_color)
                if scale != 1.0:
                    w, h = surf.get_size()
                    scaled = pygame.transform.scale(surf, (int(w * scale), int(h * scale)))
                    rect = scaled.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*70))
                else:
                    rect = surf.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*70))

                glow_rect = rect.inflate(50, 25)
                glow_color = (btn_color.r, btn_color.g, btn_color.b) if i == selected else (40,40,40)
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=12, width=2 if i==selected else 1)

                if scale != 1.0:
                    screen.blit(scaled, rect)
                else:
                    screen.blit(surf, rect)
                button_rects.append(glow_rect)

            # Hint
            hint = fonts["small"].render("Press ESC to return to menu", True, TEXT_SECONDARY)
            hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
            screen.blit(hint, hint_rect)

            pygame.display.flip()
            
            