import pygame
from characters.colidable import Colidable
from settings import *
from support import import_folder

class Particle(Colidable):
    #TO DO
    def __init__(self, path, pos, direction, damage, groups, group):
        super().__init__(path + '/particle0.png', pos, PARTICLE_SPEED, groups)
        self.direction = direction
        self.group = group
        self.eliminate = False
        self.max_dist = 15*TILESIZE
        self.damage = damage
        self.frame_index = 0
        self.animate_speed = 6/FPS
        self.animation = import_folder(path)
        
    def collision(self, direction, sprite):
        sprite.get_damaged(self.damage)
        self.eliminate = True
    
    def check_kill(self, pos):
        if self.eliminate:
            return True
        
        if ((self.rect.center[0]-pos[0])**2 + (self.rect.center[1]-pos[1])**2)**0.5 > self.max_dist:
            return True
        
        return False
    
    def animate(self):
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]
    
    def update(self):
        self.animate()
        self.move(self.group)
        