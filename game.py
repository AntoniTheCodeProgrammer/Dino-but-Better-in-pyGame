import os
import sys
import pygame
import random
# import math

from scripts.entities import Player
from scripts.utils import load_image, load_images, load_spritesheet, rotate_images, Animation
from scripts.ground import Ground
from scripts.hearts import Hearts
from scripts.objects import Obstacle, Coin
from scripts.shop import buy_item

if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Cat run")
        self.screen = pygame.display.set_mode((1280, 720))
        self.display = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 180))

        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font(None, 24)
        self.font2 = pygame.font.Font(None, 16)
        
        raw_bg = load_image('background.jpg')
        new_width = int(raw_bg.get_width() * (240 / raw_bg.get_height()))
        clean_bg = pygame.transform.smoothscale(raw_bg, (new_width, 240))

        self.assets = {
            'obstacle': load_images('obstacles', colorkey=(0,0,0)),
            'heart': load_image('hearts/heart.png'),
            'coin': load_image('coin/coin3.png'),
            'coin/sheet': Animation(load_spritesheet('coin/coin-Sheet.png', 16, 16), img_dur=10),
            'background': clean_bg,

            'grass': load_image('grass.png'),
            'hearts': load_images('hearts/background'),

            'player/run': Animation(load_spritesheet('cat/run.png', 32, 32), img_dur=6),
            'player/jump': Animation(load_spritesheet('cat/jump.png', 32, 32)),

            'fire/start': Animation(rotate_images(load_spritesheet('fire/start.png', 15, 24), -90), img_dur=6, loop=False),
            'fire/loop': Animation(rotate_images(load_spritesheet('fire/loop.png', 15, 24), -90), img_dur=6, loop=True),
            'fire/end': Animation(rotate_images(load_spritesheet('fire/end.png', 15, 24), -90), img_dur=6, loop=False),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }

        self.sfx['jump'].set_volume(0.7)
        self.sfx['ambience'].set_volume(0.2)
        
        self.coins = 20

        self.double_jump = False
        self.normal_walk = -1
        self.flametrower = False
        self.flametrower_cooldown = 0
        self.flame = 0
        self.lives = 1
        self.fast_boots = 2
        self.hearts_count = 32

        self.items = [
            {'name': 'double jump', 'price': 3, 'bought': False}, 
            {'name': 'normal walk', 'price': 1, 'bought': False}, 
            {'name': 'flametrower', 'price': 7, 'bought': False}, 
            {'name': 'extra life', 'price': 5, 'bought': False}, 
            {'name': 'fast boots', 'price': 4, 'bought': False}, 
            {'name': 'more hearts', 'price': 10, 'bought': False}
            ]

        self.player = Player(self, (50,50), (14,14), animation_offset=(-9,-14))
        self.ground = Ground(self, 164)

        self.screenshake = 0
        self.state = 'game'
        self.load_level()
        self.invincibility = 0
        self.high_score = 0

    def load_level(self):
        self.player.pos = [30, 140]
        self.player.velocity = [0, 0]
        self.player.air_time = 0
        self.movement = [0,0]
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        self.points = 0
        
        self.obstacles = []
        self.cooldown = 0
        self.level = 1
        
        self.coinsObjects = []

        self.hearts = Hearts(self.assets['hearts'], count=self.hearts_count)

    def game_loop(self):
        while self.state == 'game':
            self.display.fill((0,0,0,0))
            self.display_2.blit(self.assets['background'], (0,0))
            self.ground.render(self.display)
            
            # to moze zostac
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                text_img = self.font1.render('YOU LOST', True, (255, 225, 205))
                text_rect = text_img.get_rect(center=(self.display.get_width() // 2, 45))
                self.display.blit(text_img, text_rect)
                text_img = self.font1.render(f'Points: {int(self.points)}', True, (255, 255, 255))
                text_rect = text_img.get_rect(center=(self.display.get_width() // 2, 70))
                self.display.blit(text_img, text_rect)
                text_img = self.font2.render('press space to restart', True, (55, 155, 255))
                text_rect = text_img.get_rect(center=(self.display.get_width() // 2, 100))
                self.display.blit(text_img, text_rect)
                text_img = self.font2.render('press s to go shopping', True, (55, 155, 255))
                text_rect = text_img.get_rect(center=(self.display.get_width() // 2, 120))
                self.display.blit(text_img, text_rect)              
                        
            # moze zostac
            self.hearts.update()
            self.hearts.render(self.display_2)
            
            # tu poruszanie sie mapy
            if self.cooldown == 0:
                if random.random() < 0.01:
                    self.obstacles.append(Obstacle(self, [400, 152], 0))
                    self.cooldown = 120 / self.level
                elif random.random() < 0.01:
                    self.obstacles.append(Obstacle(self, [400, 120], 1))
                    self.cooldown = 120 / self.level
                    if random.random() < 0.5:
                        self.coinsObjects.append(Coin(self, [407, 100]))
                elif random.random() < 0.01:
                    self.obstacles.append(Obstacle(self, [400, 148], 2))
                    self.cooldown = 60 / self.level
                elif random.random() < 0.01:
                    self.coinsObjects.append(Coin(self, [400, 145]))
                    self.cooldown = 10 / self.level
            else:
                self.cooldown -= 1

            if self.invincibility > 0:
                self.invincibility -= 1

            for obstacle in self.obstacles.copy():
                obstacle.update(alive=self.dead, speed=self.level)
                if obstacle.pos[0] < -50:
                    self.obstacles.remove(obstacle)
                
                if self.invincibility == 0:
                    if self.player.rect().colliderect(obstacle.rect):
                        self.lives -= 1
                        self.invincibility = 120
                        if self.lives == 0:
                            self.dead = 1

                if self.invincibility > 0:
                    if self.invincibility % 10 < 5:
                        obstacle.render(self.display)
                else:
                    obstacle.render(self.display)

            for coin in self.coinsObjects.copy():
                coin.update(alive=self.dead, speed=self.level)
                if coin.pos[0] < -50:
                    self.coinsObjects.remove(coin)
                if self.player.rect().colliderect(coin.rect):
                    self.coinsObjects.remove(coin)
                    self.coins += 1
                coin.render(self.display)


            # do edycji
            if not self.dead:
                self.player.update(movement=[(self.movement[1]-self.movement[0]) / self.fast_boots * self.normal_walk, 0])
                self.points += 0.03
                self.player.update_flamethrower()
        
                self.level = self.points // 100 + 1
            
            self.player.render(self.display)

            # points display
           
            # --- AKTUALIZACJA REKORDU ---
            if self.points > self.high_score:
                self.high_score = self.points

            # --- UI (LEWY GÓRNY RÓG - Monety i Serca) ---
            ui_padding = 8 
            
      
            coin_img = self.assets['coin']
            self.display.blit(coin_img, (ui_padding, ui_padding))
            coin_text = self.font2.render(f'{int(self.coins)}', True, (255, 255, 255))
            self.display.blit(coin_text, (ui_padding + coin_img.get_width() + 5, ui_padding + 2))

            heart_img = self.assets['heart']
            heart_y = ui_padding + 20 
            self.display.blit(heart_img, (ui_padding, heart_y))
            life_text = self.font2.render(f'{self.lives}', True, (255, 255, 255))
            self.display.blit(life_text, (ui_padding + heart_img.get_width() + 5, heart_y + 2))

            # --- UI (PRAWY GÓRNY RÓG - Punkty) ---
            
            score_text = self.font2.render(f'Score: {int(self.points)}', True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(self.display.get_width() - ui_padding, ui_padding))
            self.display.blit(score_text, score_rect)

            hi_score_text = self.font2.render(f'HI: {int(self.high_score)}', True, (200, 200, 200))
            hi_score_rect = hi_score_text.get_rect(topright=(self.display.get_width() - ui_padding, ui_padding + 15))
            self.display.blit(hi_score_text, hi_score_rect)

            # border
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0,0,0,100), unsetcolor=(0,0,0,0))

            for offset in [(-1,0), (1,0), (0,-1), (0,1)]:
                self.display_2.blit(display_sillhouette, offset)
            
            
            # controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        if not self.dead:
                            self.player.jump()
                        else:
                            self.load_level()      
                    if event.key == pygame.K_r:
                        self.load_level()
                        self.transition = -30
                    if event.key == pygame.K_s:
                        if self.dead:
                            self.state = 'shop'
                    if event.key == pygame.K_f and self.flametrower and self.flametrower_cooldown == 0:
                       if not self.dead:
                            self.player.active_flametrower()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                        
           
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))
            
            self.display_2.blit(self.display, (0,0))

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (self.screenshake,self.screenshake))
            pygame.display.update()
            self.clock.tick(60)

    def shop_loop(self):
        # 1. Konfiguracja wymiarów
        # Zmniejszyłem szerokość na 90, żeby zmieściło się z marginesami na ekranie 320px
        ITEM_SIZE_X = 90
        ITEM_SIZE_Y = 50
        GAP = 10
        COLS = 3

        # 2. Matematyka centrowania (Klucz do sukcesu)
        # Obliczamy szerokość całej grupy przedmiotów: (szerokość * ilość) + (odstępy)
        grid_width = (ITEM_SIZE_X * COLS) + (GAP * (COLS - 1))
        
        # Wyliczamy START_X: (Szerokość ekranu - Szerokość grupy) / 2
        START_X = (self.display.get_width() - grid_width) // 2
        START_Y = 55 

        while self.state == 'shop':
            self.display.fill((50, 50, 100))

            # Obsługa myszki (skalowanie)
            mouse_pos = pygame.mouse.get_pos()
            scale_x = self.display.get_width() / self.screen.get_width()
            scale_y = self.display.get_height() / self.screen.get_height()
            game_mouse = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)

            # --- RYSOWANIE NAGŁÓWKA ---
            title_img = self.font1.render('SHOP', True, (255, 185, 165))
            text_rect = title_img.get_rect(center=(self.display.get_width() // 2, 25))
            self.display.blit(title_img, text_rect)

            # --- RYSOWANIE MONET (OBRAZEK + TEKST) ---
            ui_padding = 8 

            coin_img = self.assets['coin']
            self.display.blit(coin_img, (ui_padding, ui_padding))
            coin_text = self.font2.render(f'{int(self.coins)}', True, (255, 255, 255))
            self.display.blit(coin_text, (ui_padding + coin_img.get_width() + 5, ui_padding + 2))

            heart_img = self.assets['heart']
            heart_y = ui_padding + 20 
            self.display.blit(heart_img, (ui_padding, heart_y))
            life_text = self.font2.render(f'{self.lives}', True, (255, 255, 255))
            self.display.blit(life_text, (ui_padding + heart_img.get_width() + 5, heart_y + 2))

            # --- PĘTLA PRZEDMIOTÓW (GRID) ---
            for i, item in enumerate(self.items):
                row = i // COLS
                col = i % COLS

                # Używamy wyliczonego START_X
                x = START_X + col * (ITEM_SIZE_X + GAP)
                y = START_Y + row * (ITEM_SIZE_Y + GAP)

                item_rect = pygame.Rect(x, y, ITEM_SIZE_X, ITEM_SIZE_Y)

                # Rysowanie tła przycisku
                if item_rect.collidepoint(game_mouse):
                    pygame.draw.rect(self.display, (255, 255, 255), item_rect)
                    text_color = (50, 50, 100)
                else:
                    pygame.draw.rect(self.display, (50, 50, 50), item_rect)
                    text_color = (255, 255, 255)

                # Kolory tekstu zależnie od stanu (Kupiony / Stać nas / Nie stać nas)
                if item['bought']:
                    name_color = (255, 80, 80)
                elif self.coins >= item['price']:
                    name_color = (80, 255, 80)
                else:
                    name_color = (150, 150, 150)

                name_img = self.font2.render(item['name'], True, name_color)
                self.display.blit(name_img, (x + 5, y + 5))
                
                price_text = "SOLD" if item['bought'] else str(item['price'])
                price_img = self.font2.render(price_text, True, text_color)
                self.display.blit(price_img, (x + 5, y + 25))


            # --- FINALIZACJA KLATKI ---
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            
            # --- OBSŁUGA KLAWISZY ---
            # 1. KLAWIATURA
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                        self.state = 'game'
                    
                    key_index = event.key - 49 
                    buy_item(self, key_index)

                # 2. MYSZKA (NOWOŚĆ)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        for i, item in enumerate(self.items):
                            row = i // COLS
                            col = i % COLS
                            x = START_X + col * (ITEM_SIZE_X + GAP)
                            y = START_Y + row * (ITEM_SIZE_Y + GAP)
                            item_rect = pygame.Rect(x, y, ITEM_SIZE_X, ITEM_SIZE_Y)
                            
                            if item_rect.collidepoint(game_mouse):
                                buy_item(self, i)
                        
            self.clock.tick(60)

    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.sfx['ambience'].play(-1)

        while True:
            if self.state == 'game':
                self.load_level()
                self.game_loop()
            elif self.state == 'shop':
                self.shop_loop()

Game().run()