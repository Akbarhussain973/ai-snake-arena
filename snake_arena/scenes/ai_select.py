# scenes/ai_select.py (animated)
import pygame
import random
import math
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, ASTAR_ID, GREEDY_ID, MINIMAX_ID

class AISelectScene:
    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        # Default selections: A* and Greedy enabled, Minimax disabled
        selected_ais = {
            "astar": True,
            "greedy": True,
            "minimax": False
        }
        ai_list = [("astar", "A* Snake"), ("greedy", "Greedy Snake"), ("minimax", "Minimax Snake")]
        current_index = 0

        # Animation variables
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
                    if event.key == pygame.K_UP:
                        current_index = (current_index - 1) % len(ai_list)
                    elif event.key == pygame.K_DOWN:
                        current_index = (current_index + 1) % len(ai_list)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        key = ai_list[current_index][0]
                        selected_ais[key] = not selected_ais[key]
                    elif event.key == pygame.K_c:
                        enabled = []
                        if selected_ais["astar"]:
                            enabled.append(ASTAR_ID)
                        if selected_ais["greedy"]:
                            enabled.append(GREEDY_ID)
                        if selected_ais["minimax"]:
                            enabled.append(MINIMAX_ID)
                        return enabled
                    elif event.key == pygame.K_ESCAPE:
                        return "menu"

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
            title_text = "CHOOSE YOUR OPPONENTS"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 80))
                start_x += char_surf.get_width()

            # Subtitle
            sub_font = fonts["body"]
            sub_text = sub_font.render("Press SPACE to toggle • C to confirm", True, TEXT_SECONDARY)
            sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH//2, 150))
            screen.blit(sub_text, sub_rect)

            # AI list with pulsing checkboxes
            y = 220
            for i, (key, label) in enumerate(ai_list):
                # Scale pulsing for selected item
                scale = 1 + 0.05 * math.sin(pulse) if i == current_index else 1.0
                color = ACCENT if i == current_index else TEXT_PRIMARY
                checkbox = "[✓]" if selected_ais[key] else "[ ]"
                text = f"{checkbox} {label}"
                surf = fonts["heading"].render(text, True, color)
                if scale != 1.0:
                    w, h = surf.get_size()
                    scaled_surf = pygame.transform.scale(surf, (int(w * scale), int(h * scale)))
                    rect = scaled_surf.get_rect(center=(WINDOW_WIDTH//2, y))
                    screen.blit(scaled_surf, rect)
                else:
                    rect = surf.get_rect(center=(WINDOW_WIDTH//2, y))
                    screen.blit(surf, rect)
                y += 60

            # Instructions
            hint1 = fonts["small"].render("Use ↑ ↓ to move • SPACE to toggle • C to confirm", True, TEXT_SECONDARY)
            hint1_rect = hint1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT-70))
            screen.blit(hint1, hint1_rect)

            hint2 = fonts["small"].render("ESC to go back", True, TEXT_SECONDARY)
            hint2_rect = hint2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT-40))
            screen.blit(hint2, hint2_rect)

            pygame.display.flip()
            