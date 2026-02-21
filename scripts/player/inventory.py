class Inventory:
    def __init__(self):
        self.items = []
        self.active_skill = None
        self.coins = 0

    def apply_passives(self, game):
        if 'double_jump' in self.items:
            game.stats.jumps += 1
            
        if 'fast_boots' in self.items:
            game.stats.speed += 0.5
            
        if 'extra_life' in self.items:
            game.stats.health += 1