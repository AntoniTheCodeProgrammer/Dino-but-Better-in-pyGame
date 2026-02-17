import random

class Heart:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth
        
    def update(self):
        self.pos[1] += self.speed
        # self.pos[0] += random.random() - 0.5
        
    def render(self, surf, offset= (0,0)):
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()), render_pos[1] % (surf.get_height() + self.img.get_height())))
        
class Hearts:
    def __init__(self, heart_images, count=16):
        self.hearts = []
        
        for _ in range(count):
            self.hearts.append(Heart((random.random() * 99999, random.random() * 99999), random.choice(heart_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
            
        self.hearts.sort(key=lambda x: x.depth)
        
    def update(self):
        for heart in self.hearts:
            heart.update()
            
    def render(self, surf, offset=(0,0)):
        for heart in self.hearts:
            heart.render(surf, offset=offset)