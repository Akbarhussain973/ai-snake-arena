# scenes/high_scores.py (animated)
import pygame
import random
import math
import json
import os
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY

class HighScoresScene:
    def run(self, screen, fonts):
        clock = pygame.time.Clock()
        scores = self._load_scores()
        hue = 0
        particles = []
        for _ in range(50):
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
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN:
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
            title_text = "HIGH SCORES"
            total_width = sum(title_font.size(c)[0] for c in title_text)
            start_x = (WINDOW_WIDTH - total_width) // 2
            for i, char in enumerate(title_text):
                char_hue = (hue + i * 15) % 360
                color = pygame.Color(0)
                color.hsla = (char_hue, 100, 50, 100)
                char_surf = title_font.render(char, True, color)
                screen.blit(char_surf, (start_x, 80))
                start_x += char_surf.get_width()

            # Player vs AI
            y = 160
            mode_title = fonts["heading"].render("Player vs AI (Top Scores)", True, TEXT_PRIMARY)
            screen.blit(mode_title, (WINDOW_WIDTH//2 - mode_title.get_width()//2, y))
            y += 40
            for i, entry in enumerate(scores.get("pvai", [])[:5]):
                line = f"{i+1}. {entry['name']} - {entry['score']}"
                surf = fonts["body"].render(line, True, TEXT_SECONDARY)
                screen.blit(surf, (WINDOW_WIDTH//2 - surf.get_width()//2, y))
                y += 30
            if not scores.get("pvai"):
                no = fonts["body"].render("No scores yet. Play a game!", True, TEXT_SECONDARY)
                screen.blit(no, (WINDOW_WIDTH//2 - no.get_width()//2, y))

            y += 60
            mode_title2 = fonts["heading"].render("AI Battle (Recent Winners)", True, TEXT_PRIMARY)
            screen.blit(mode_title2, (WINDOW_WIDTH//2 - mode_title2.get_width()//2, y))
            y += 40
            for entry in scores.get("aibattle", [])[-5:]:
                line = f"{entry['winner']} (Winner)"
                surf = fonts["body"].render(line, True, TEXT_SECONDARY)
                screen.blit(surf, (WINDOW_WIDTH//2 - surf.get_width()//2, y))
                y += 30
            if not scores.get("aibattle"):
                no = fonts["body"].render("No battles recorded.", True, TEXT_SECONDARY)
                screen.blit(no, (WINDOW_WIDTH//2 - no.get_width()//2, y))

            back = fonts["small"].render("Press ESC or click anywhere to return", True, TEXT_SECONDARY)
            back_rect = back.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
            screen.blit(back, back_rect)

            pygame.display.flip()

    def _load_scores(self):
        scores = {"pvai": [], "aibattle": []}
        if os.path.exists("high_scores.json"):
            try:
                with open("high_scores.json", "r") as f:
                    data = json.load(f)
                    if "pvai" in data:
                        scores["pvai"] = data["pvai"]
                    if "aibattle" in data:
                        scores["aibattle"] = data["aibattle"]
            except:
                pass
        return scores
    
    