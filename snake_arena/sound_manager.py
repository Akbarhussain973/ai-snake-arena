# sound_manager.py
import pygame
import math
import array
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.enabled = True
        self.music_playing = False
        self._load_sounds()
        self._load_music()

    def _generate_beep(self, frequency, duration):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0]) * n_samples * 2
        for i in range(n_samples):
            t = float(i) / sample_rate
            value = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * t))
            buf[i*2] = value
            buf[i*2 + 1] = value
        return pygame.mixer.Sound(buffer=buf)

    def _load_sounds(self):
        sound_dir = "assets/sounds"
        try:
            if not os.path.exists(sound_dir):
                os.makedirs(sound_dir)
            for name in ["eat", "death", "levelup"]:
                path = os.path.join(sound_dir, f"{name}.wav")
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    if name == "eat":
                        freq, dur = 880, 0.15
                    elif name == "death":
                        freq, dur = 220, 0.4
                    else:
                        freq, dur = 440, 0.25
                    self.sounds[name] = self._generate_beep(freq, dur)
        except Exception as e:
            print(f"Sound error: {e}")
            self.enabled = False

    def _load_music(self):
        """Load background music (supports .mp3, .ogg, .wav)."""
        music_path = "assets/music/background.mp3"
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            self.music_playing = True
        else:
            # If no music file, we can generate a simple tone loop (optional)
            # But we'll just skip music.
            print("No background music found. Add background.mp3 to assets/music/")
            self.music_playing = False

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def start_music(self):
        if self.music_playing and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # loop forever

    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            
            