class Upgrades:
    def __init__(self):
        self.health = 0
        self.demage = 0
        self.jumps = 0
        self.speed = 0

    def to_dict(self):
        return {
            "health": self.health,
            "damage": self.damage,
            "jumps": self.jumps,
            "speed": self.speed
        }
        
    def load_dict(self, data):
        self.health = data.get("health", 1)
        self.damage = data.get("damage", 1)
        self.jumps = data.get("jumps", 1)
        self.speed = data.get("speed", 1)

    def apply_passives(self, game):
        game.stats.health += self.health
        game.stats.demage += self.demage
        game.stats.jumps += self.jumps
        game.stats.speed += self.speed