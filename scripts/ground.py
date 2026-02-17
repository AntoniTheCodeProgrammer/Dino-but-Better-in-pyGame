class Ground:
    def __init__(self, game, y_pos):
        self.game = game
        self.y_pos = y_pos
        self.image = self.game.assets['grass']
        self.width = self.image.get_width()
        self.x = 0

    def render(self, surf):
        for i in range(20):
            surf.blit(self.image, (self.x + self.width * i, self.y_pos))
            