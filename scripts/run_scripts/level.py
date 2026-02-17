# scripts/level.py
from scripts.run_scripts.hearts import Hearts

def load_level(game):
    game.player.pos = [30, 140]
    game.player.velocity = [0, 0]
    game.player.air_time = 0
    game.movement = [0,0]
    
    game.dead = 0
    game.transition = -30
    game.points = 0
    
    game.obstacles = []
    game.cooldown = 0
    
    game.coinsObjects = []

    game.hearts = Hearts(game.assets['hearts'], count=game.hearts_count)