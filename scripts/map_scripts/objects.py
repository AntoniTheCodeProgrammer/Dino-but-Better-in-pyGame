import pygame

class Gate:
    def __init__(self, game, pos, id):
        self.pos = [pos[0], pos[1]]
        
        if id in game.unlocked_gates:
            self.unlocked = True
            self.image = game.assets['open']
        else:
            self.unlocked = False
            self.image = game.assets['closed']

        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

    def render(self, surf, render_scroll = [0, 0]):
        surf.blit(self.image, (self.pos[0] - render_scroll[0], self.pos[1] - render_scroll[1]))

class Level:
    def __init__(self, game, pos, id, lv):
        self.animation = game.assets[id].copy()
        self.pos = [pos[0], pos[1]]
        self.level = lv
        first_frame = self.animation.img()

        self.rect = pygame.Rect(self.pos[0], self.pos[1], first_frame.get_width(), first_frame.get_height())

    def update(self):
        self.animation.update()

    def use(self, game):
        game.level = self.level
        game.state = "game"

    def render(self, surf, render_scroll = [0, 0]):
        surf.blit(self.animation.img(), (self.pos[0] - render_scroll[0], self.pos[1] - render_scroll[1]))

class Shop:
    def __init__(self, game, pos, id):
        self.animation = game.assets[id].copy()
        self.pos = [pos[0], pos[1]]
        self.id = id

        first_frame = self.animation.img()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], first_frame.get_width(), first_frame.get_height())

    def update(self):
        self.animation.update()

    def use(self, game):
        match self.id:
            case "shop_01":
                game.state = "shop"

    def render(self, surf, render_scroll = [0, 0]):
        surf.blit(self.animation.img(), (self.pos[0] - render_scroll[0], self.pos[1] - render_scroll[1]))