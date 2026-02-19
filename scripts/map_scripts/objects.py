import pygame

class Gate:
    def __init__(self, game, pos, id):
        self.pos = [pos[0], pos[1]]
        
        if id in game.unlocked_gates:
            self.unlocked = True
        else:
            self.unlocked = False
            
        if self.unlocked:
            self.image = game.assets['open']
        else:
            self.image = game.assets['closed']

        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

    def render(self, surf, render_scroll = [0, 0]):
        # Rysujemy drzwi
        surf.blit(self.image, [self.pos[0] + render_scroll[0], self.pos[1] + render_scroll[1]])