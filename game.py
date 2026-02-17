# game.py
import os
import sys
import pygame

# Importy z naszych skryptów
from scripts.run_scripts.entities import Player
from scripts.utils import load_image, load_images, load_spritesheet, rotate_images, Animation
from scripts.run_scripts.ground import Ground

# Importy z nowych plików
from scripts.shop_scripts.config import SHOP_ITEMS
from scripts.run_scripts.level import load_level
from scripts.loops.run_loop import game_loop
from scripts.loops.shop_loop import shop_loop

# Fix dla PyInstaller (jeśli będziesz robił EXE)
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cat run")
        
        # Ekran
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 180))

        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font(None, 24)
        self.font2 = pygame.font.Font(None, 16)
        
        # Tło (skalowane)
        raw_bg = load_image('background.jpg')
        new_width = int(raw_bg.get_width() * (240 / raw_bg.get_height()))
        clean_bg = pygame.transform.smoothscale(raw_bg, (new_width, 240))

        # Ładowanie Assetów (Słownik)
        self.assets = {
            'obstacle': load_images('obstacles', colorkey=(0,0,0)),
            'heart': load_image('hearts/heart.png'),
            'coin': load_image('coin/coin3.png'),
            'coin/sheet': Animation(load_spritesheet('coin/coin-Sheet.png', 16, 16), img_dur=10),
            'background': clean_bg,
            'grass': load_image('grass.png'),
            'hearts': load_images('hearts/background'),
            
            # Animacje Kota
            'player/run': Animation(load_spritesheet('cat/run.png', 32, 32), img_dur=6),
            'player/jump': Animation(load_spritesheet('cat/jump.png', 32, 32)),
            
            # Animacje Ognia
            'fire/start': Animation(rotate_images(load_spritesheet('fire/start.png', 15, 24), -90), img_dur=6, loop=False),
            'fire/loop': Animation(rotate_images(load_spritesheet('fire/loop.png', 15, 24), -90), img_dur=6, loop=True),
            'fire/end': Animation(rotate_images(load_spritesheet('fire/end.png', 15, 24), -90), img_dur=6, loop=False),
        }

        # Dźwięki
        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        self.sfx['jump'].set_volume(0.7)
        self.sfx['ambience'].set_volume(0.2)
        
        # Zmienne Gracza (Ekwipunek)
        self.coins = 20
        self.double_jump = False
        self.normal_walk = -1
        self.flametrower = False
        self.flametrower_cooldown = 0
        self.flame = 0
        self.lives = 1
        self.fast_boots = 2
        self.hearts_count = 32
        
        # Sklep (z pliku config)
        self.items = SHOP_ITEMS

        # Inicjalizacja obiektów
        self.player = Player(self, (50,50), (14,14), animation_offset=(-9,-14))
        self.ground = Ground(self, 164)

        self.screenshake = 0
        self.state = 'game'
        self.invincibility = 0
        self.high_score = 0
        
        # Start
        load_level(self)

    def run(self):
        # Muzyka
        try:
            pygame.mixer.music.load('data/music.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception:
            print("Brak pliku muzyki, pomijam.")

        self.sfx['ambience'].play(-1)

        while True:
            # MANAGER STANÓW
            if self.state == 'game':
                game_loop(self)
            elif self.state == 'shop':
                shop_loop(self)

# Uruchomienie gry
if __name__ == "__main__":
    Game().run()