class Stats:
    def __init__(self):
        self.health = 1
        self.demage = 1
        self.jumps = 1
        self.speed = 1

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

    def reset(self):
        self.health = 1
        self.demage = 1
        self.jumps = 1
        self.speed = 1