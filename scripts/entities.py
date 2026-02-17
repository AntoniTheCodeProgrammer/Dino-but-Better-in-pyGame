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

        if self.pos[0] < 0:
            self.pos[0] = 0
        
        if self.pos[0] > 300:
            self.pos[0] = 300

                
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
        if self.game.double_jump:
            self.jumps = 2
        else:
            self.jumps = 1
        self.animation_offset = animation_offset

        # FLAMETROWER
        self.flame_active = False
        self.flame_state = 'none'
        self.flame_timer = 0
        self.flame_animation = None
        
        self.flame_offset = (16, -5)
        
    def update(self, movement=(0,0)):
        super().update(movement=movement)
     
        self.air_time += 1
        
        if self.collisions['down']:
            self.air_time = 0
            if self.game.double_jump:
                self.jumps = 2
            else:
                self.jumps = 1
          
        if self.air_time > 4:
            self.set_action('jump')
        else:
            self.set_action('run')

    def render(self, surf):
        if self.flame_active and self.flame_animation:
            fire_x = self.pos[0] + self.size[0] + self.animation_offset[0] + self.flame_offset[0]
            fire_y = self.pos[1] + self.flame_offset[1]
                
            surf.blit(self.flame_animation.img(), (fire_x, fire_y))

        return super().render(surf)
        

    def jump(self):
        if self.jumps:
            self.game.sfx['jump'].play()
            self.velocity[1] = -3.5
            self.jumps -= 1
            self.air_time = 5

    def active_flametrower(self):
        if not self.flame_active:
            self.flame_active = True
            self.flame_state = 'start'
            self.flame_animation = self.game.assets['fire/start'].copy()
            self.flame_timer = 120

            # dzwiek

    def update_flamethrower(self):
        if not self.flame_active:
            return
        
        self.flame_animation.update()

        if self.flame_state == 'start':
            if self.flame_animation.done:
                self.flame_state = 'loop'
                self.flame_animation = self.game.assets['fire/loop'].copy()
        
        # 2. FAZA LOOP (Główny ogień)
        elif self.flame_state == 'loop':
            self.flame_timer -= 1
            
            current_fire_img = self.flame_animation.img()
            fire_rect = current_fire_img.get_rect()

            fire_rect.left = self.pos[0] + self.size[0] + self.animation_offset[0]
            fire_rect.y = self.pos[1] + self.flame_offset[1]

            for obstacle in self.game.obstacles.copy():
                if fire_rect.colliderect(obstacle.rect):
                     self.game.obstacles.remove(obstacle)
            
            if self.flame_timer <= 0:
                self.flame_state = 'end'
                self.flame_animation = self.game.assets['fire/end'].copy()

        # 3. FAZA END
        elif self.flame_state == 'end':
            if self.flame_animation.done:
                self.flame_active = False
                self.flame_state = 'none'
                self.flame_animation = None
    
        