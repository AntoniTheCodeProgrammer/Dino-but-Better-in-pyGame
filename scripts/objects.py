import pygame


class Obstacle:
    def __init__(self, game, pos, id):
        self.pos = pos
        self.image = game.assets['obstacle'][id]
        self.game = game
        self.rect = self.image.get_rect(topleft=pos)

        if id == 1:
            self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height()/2)
        else:
            self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

    
    def update(self, alive = 0, speed = 1):
        if alive == 0:
            self.pos[0] -= max(1, 1 * (speed / 2))
            self.rect.x = self.pos[0]

    def render(self, surf):
        surf.blit(self.image, self.pos)
    

class Coin:
    def __init__(self, game, pos):
        self.pos = pos
        self.game = game
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 16)
        self.animation = self.game.assets['coin/sheet'].copy()

        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
    
    def update(self, alive = 0, speed = 1):
        if alive == 0:
            self.pos[0] -= max(1, 1 * (speed / 2))
            self.rect.x = self.pos[0]
        self.animation.update()

    def render(self, surf):
        surf.blit(self.animation.img(), self.pos)
