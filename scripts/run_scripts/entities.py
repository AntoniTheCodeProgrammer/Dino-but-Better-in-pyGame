import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action('run')

        self.last_movement = [0,0]
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, movement = (0,0), floor_y = 164):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.last_movement = movement

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        bottom_edge = self.pos[1] + self.size[1]
        
        if bottom_edge > floor_y:
            self.pos[1] = floor_y - self.size[1]
            self.velocity[1] = 0
            self.collisions['down'] = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1) 
        if self.collisions['down']:
            self.velocity[1] = 0
    
        self.animation.update()
        
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] + self.animation_offset[0], self.pos[1] + self.animation_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size, animation_offset=(-3,-3)):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.animation_offset = animation_offset
        
    def update(self, movement=(0,0)):
        super().update(movement=movement)
     
        if self.pos[0] < 0:
            self.pos[0] = 0
        
        if self.pos[0] > 300:
            self.pos[0] = 300
            
        self.air_time += 1
        
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
          
        if self.air_time > 4:
            self.set_action('jump')
        else:
            self.set_action('run')

    def jump(self):
        if self.jumps:
            self.game.sfx['jump'].play()
            self.velocity[1] = -3.5
            self.jumps -= 1
            self.air_time = 5        