# game.py
import os
import sys
import pygame

# Importy z naszych skryptów
from scripts.player.inventory import Inventory
from scripts.player.stats import Stats
from scripts.utils import load_image, load_images, load_spritesheet, rotate_images, Animation

from scripts.loops.run_loop import run_loop
from scripts.loops.shop_loop import shop_loop
from scripts.loops.start_loop import start_loop
from scripts.loops.map_loop import map_loop

# Fix dla PyInstaller (jeśli będziesz robił EXE)
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Cat run")
        
        # Ekran
        self.screen = pygame.display.set_mode((1600, 900))
        self.display = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 180))

        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font(None, 24)
        self.font2 = pygame.font.Font(None, 16)
        
        # Tło (skalowane)
        raw_bg = load_image('backgrounds/background.jpg')
        new_width = int(raw_bg.get_width() * (240 / raw_bg.get_height()))
        clean_bg = pygame.transform.smoothscale(raw_bg, (new_width, 240))

        # Ładowanie Assetów
        self.assets = {
            'obstacle': load_images('obstacles', colorkey=(0,0,0)),
            'heart': load_image('hearts/heart.png'),
            'coin': load_image('coin/coin3.png'),
            'coin/sheet': Animation(load_spritesheet('coin/coin-Sheet.png', 16, 16), img_dur=10),
            'background': clean_bg,
            'hearts': load_images('hearts/background'),

            'grass': load_image('blocks/grass.png'),
            'stone1': load_image('blocks/stone1.png'),
            'stone2': load_image('blocks/stone2.png'),
            'stone_grass1': load_image('blocks/stone_grass1.png'),
            'stone_grass2': load_image('blocks/stone_grass2.png'),
            'stone_grass3': load_image('blocks/stone_grass3.png'),
            
            'open': load_image('doors/Doors_open.png'),
            'closed': load_image('doors/Doors_closed.png'),

            'shop_01': Animation(load_spritesheet('objects/shop_01.png', 32, 32), img_dur=6),
            
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
        
        # Zmienne Gracza
        self.inventory = Inventory()
        self.stats = Stats()      

        self.transition = -30

        self.level = 0
        self.state = 'start'
        
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
                run_loop(self)
            elif self.state == 'shop':
                shop_loop(self)
            elif self.state == 'start':
                start_loop(self)
            elif self.state == 'map':
                map_loop(self)

# Uruchomienie gry
if __name__ == "__main__":
    Game().run()