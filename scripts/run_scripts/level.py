import random

from scripts.run_scripts.hearts import Hearts
from scripts.run_scripts.objects import Obstacle, Coin, Platform

def load_level(game):
    game.player.pos = [30, 140]
    game.player.velocity = [0, 0]
    game.player.air_time = 0
    game.movement = [0,0]
    
    game.dead = 0
    game.transition = -30
    game.points = 0
    
    game.obstacles = []
    game.platforms = []
    game.cooldown = 0
    
    game.coinsObjects = []

    game.hearts = Hearts(game.assets['hearts'], count=32)

def gen_obstacle(game):
    if game.cooldown == 0:
        if random.random() < 0.01:
            game.obstacles.append(Obstacle(game, [400, 152], 0))
            game.cooldown = 120
        elif random.random() < 0.01:
            game.obstacles.append(Obstacle(game, [400, 120], 1))
            game.cooldown = 120
            if random.random() < 0.5:
                game.coinsObjects.append(Coin(game, [407, 100]))
        elif random.random() < 0.01:
            game.obstacles.append(Obstacle(game, [400, 148], 2))
            game.cooldown = 60
        elif random.random() < 0.01:
            game.coinsObjects.append(Coin(game, [400, 145]))
            game.cooldown = 10
    else:
        game.cooldown -= 1

def gen_platform(game):
    print(game.cooldown)
    if game.cooldown == 0:
        pos_y = random.randrange(68, 132)
        if len(game.platforms) != 0:
            if abs(game.platforms[-1].pos[1] - pos_y) > 32:
                game.platforms.append(Platform(game, pos_y))
                game.cooldown = random.choice([16, 32, 48, 64, 128])
        else:
            game.platforms.append(Platform(game, pos_y))
            game.cooldown = random.choice([16, 32, 48, 64, 128])
    else:
        game.cooldown -= 1