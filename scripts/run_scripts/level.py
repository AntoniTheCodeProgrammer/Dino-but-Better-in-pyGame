import random

from scripts.run_scripts.hearts import Hearts
from scripts.run_scripts.objects import Obstacle, Coin, Platform
from scripts.player.entities import Player

class RunLevel:
    def __init__(self, game):
        self.game = game
        self.points = 0
        self.dead = 0
        self.cooldown = 0
        
        # Listy obiektów żyją tylko w tej instancji
        self.obstacles = []
        self.platforms = []
        self.coinsObjects = []
        
        self.hearts = Hearts(game.assets['hearts'], count=32)

        self.player = Player(game, (50,50), (14,14), animation_offset=(-9,-14))

    def gen_obstacle(self):
        if self.cooldown == 0:
            if random.random() < 0.01:
                self.obstacles.append(Obstacle(self.game, [400, 152], 0))
                self.cooldown = 120
            elif random.random() < 0.01:
                self.obstacles.append(Obstacle(self.game, [400, 120], 1))
                self.cooldown = 120
                if random.random() < 0.5:
                    self.coinsObjects.append(Coin(self.game, [407, 100]))
            elif random.random() < 0.01:
                self.obstacles.append(Obstacle(self.game, [400, 148], 2))
                self.cooldown = 60
            elif random.random() < 0.01:
                self.coinsObjects.append(Coin(self.game, [400, 145]))
                self.cooldown = 10
        else:
            self.cooldown -= 1

    def gen_platform(self):
        if self.cooldown == 0:
            pos_y = random.randrange(68, 132)
            if len(self.platforms) != 0:
                if abs(self.platforms[-1].pos[1] - pos_y) > 32:
                    self.platforms.append(Platform(self.game, pos_y))
                    self.cooldown = random.choice([16, 32, 48, 64, 128])
            else:
                self.platforms.append(Platform(self.game, pos_y))
                self.cooldown = random.choice([16, 32, 48, 64, 128])
        else:
            self.cooldown -= 1