import pygame
import random
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, ACCENT, TEXT_SECONDARY
from maps import get_map_names, MAPS

class MapSelectScene:
    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        map_names = get_map_names()
        selected = 0
        button_rects = []
        hue = 0
        pulse = 0

        particles = []
        for _ in range(60):
            particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'size': random.randint(2,5),
                'speed': random.uniform(0.5,1.5),
                'color': [random.randint(150,255), random.randint(150,255), random.randint(150,255)]
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
                        selected = (selected - 1) % len(map_names)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(map_names)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return map_names[selected]
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            return map_names[i]

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
            title_text = "SELECT MAP"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 80))
                start_x += char_surf.get_width()

            # Description of selected map
            desc_font = fonts["small"]
            desc = MAPS[map_names[selected]]["description"]
            desc_surf = desc_font.render(desc, True, TEXT_SECONDARY)
            desc_rect = desc_surf.get_rect(center=(WINDOW_WIDTH//2, 140))
            screen.blit(desc_surf, desc_rect)

            # Buttons
            button_rects = []
            btn_y = 220
            for i, name in enumerate(map_names):
                scale = 1 + 0.05 * math.sin(pulse) if i == selected else 1.0
                if i == selected:
                    btn_color = pygame.Color(0)
                    btn_color.hsla = ((hue + i * 30) % 360, 100, 60, 100)
                else:
                    btn_color = TEXT_SECONDARY
                label = MAPS[name]["name"]
                surf = fonts["heading"].render(label, True, btn_color)
                if scale != 1.0:
                    w, h = surf.get_size()
                    scaled = pygame.transform.scale(surf, (int(w * scale), int(h * scale)))
                    rect = scaled.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*70))
                else:
                    rect = surf.get_rect(center=(WINDOW_WIDTH//2, btn_y + i*70))
                glow_rect = rect.inflate(60,30)
                glow_color = (btn_color.r, btn_color.g, btn_color.b) if i == selected else (40,40,40)
                pygame.draw.rect(screen, glow_color, glow_rect, border_radius=12, width=2 if i==selected else 1)
                if scale != 1.0:
                    screen.blit(scaled, rect)
                else:
                    screen.blit(surf, rect)
                button_rects.append(glow_rect)

            hint = fonts["small"].render("Press ESC to go back", True, TEXT_SECONDARY)
            hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT-50))
            screen.blit(hint, hint_rect)

            pygame.display.flip()
            
            