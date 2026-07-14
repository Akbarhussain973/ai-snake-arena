# scenes/speed_select.py
import pygame
import random
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, ACCENT, TEXT_SECONDARY

class SpeedSelectScene:
    def run(self, screen, fonts, default_speed=12):
        clock = pygame.time.Clock()
        speed = default_speed
        hue = 0
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
            for p in particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = WINDOW_HEIGHT
                    p['x'] = random.randint(0, WINDOW_WIDTH)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        speed = max(5, speed - 1)
                    elif event.key == pygame.K_RIGHT:
                        speed = min(25, speed + 1)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return speed
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                    mouse_x = event.pos[0]
                    if 200 < mouse_x < WINDOW_WIDTH - 200:
                        rel = (mouse_x - 200) / (WINDOW_WIDTH - 400)
                        speed = int(5 + rel * 20)
                        speed = max(5, min(25, speed))

            # Gradient background
            for y in range(WINDOW_HEIGHT):
                ratio = y / WINDOW_HEIGHT
                r = int(18 + 10 * ratio)
                g = int(18 + 5 * ratio)
                b = int(30 + 20 * ratio)
                pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

            # Particles
            for p in particles:
                surf = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (p['color'][0], p['color'][1], p['color'][2], 160), (p['size'], p['size']), p['size'])
                screen.blit(surf, (int(p['x']-p['size']), int(p['y']-p['size'])))

            # Rainbow title
            title_font = fonts["title"]
            title_text = "GAME SPEED"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 100))
                start_x += char_surf.get_width()

            # Slider
            slider_x = 200
            slider_y = 280
            slider_width = WINDOW_WIDTH - 400
            pygame.draw.rect(screen, (60,60,80), (slider_x, slider_y, slider_width, 12), border_radius=6)
            knob_x = slider_x + int((speed - 5) / 20 * slider_width)
            pygame.draw.circle(screen, ACCENT, (knob_x, slider_y+6), 14)
            pygame.draw.circle(screen, (255,255,255), (knob_x, slider_y+6), 14, 2)

            # Speed value
            speed_text = fonts["heading"].render(f"{speed} FPS", True, ACCENT)
            text_rect = speed_text.get_rect(center=(WINDOW_WIDTH//2, slider_y - 40))
            screen.blit(speed_text, text_rect)

            # Instructions
            instr1 = fonts["small"].render("← →  or drag slider  •  ENTER confirm  •  ESC back", True, TEXT_SECONDARY)
            instr1_rect = instr1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT-80))
            screen.blit(instr1, instr1_rect)
            instr2 = fonts["small"].render("(Overrides difficulty speed)", True, TEXT_SECONDARY)
            instr2_rect = instr2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT-50))
            screen.blit(instr2, instr2_rect)

            pygame.display.flip()
            
            