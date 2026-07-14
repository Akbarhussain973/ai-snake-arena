# scenes/name_input.py
import pygame
import random
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY

class NameInputScene:
    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        name = ""
        cursor_visible = True
        cursor_timer = 0
        hue = 0
        particles = []
        
        # Create floating particles
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
            
            # Update particles
            for p in particles:
                p['y'] -= p['speed']
                if p['y'] < 0:
                    p['y'] = WINDOW_HEIGHT
                    p['x'] = random.randint(0, WINDOW_WIDTH)
                    p['color'] = [random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            return name.strip()
                        else:
                            return "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"
                    else:
                        if event.unicode.isprintable() and len(name) < 12:
                            name += event.unicode

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
            title_text = "ENTER YOUR NAME"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 100))
                start_x += char_surf.get_width()

            # Input box
            box_rect = pygame.Rect(WINDOW_WIDTH//2 - 160, 220, 320, 60)
            pygame.draw.rect(screen, (30,30,40), box_rect, border_radius=10)
            pygame.draw.rect(screen, ACCENT, box_rect, 2, border_radius=10)

            # Render name text
            name_surf = fonts["heading"].render(name, True, TEXT_PRIMARY)
            name_rect = name_surf.get_rect(center=(WINDOW_WIDTH//2, 250))
            screen.blit(name_surf, name_rect)

            # Blinking cursor
            cursor_timer += 1
            if cursor_timer >= 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            if cursor_visible:
                cursor_x = name_rect.right + 4
                cursor_y = name_rect.centery - 18
                pygame.draw.line(screen, ACCENT, (cursor_x, cursor_y), (cursor_x, cursor_y+36), 3)

            # Instructions
            hint = fonts["small"].render("Press ENTER to confirm  |  ESC to go back", True, TEXT_SECONDARY)
            hint_rect = hint.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 60))
            screen.blit(hint, hint_rect)

            info = fonts["small"].render("This name will appear on the leaderboard", True, TEXT_SECONDARY)
            info_rect = info.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 100))
            screen.blit(info, info_rect)

            pygame.display.flip()
            
            