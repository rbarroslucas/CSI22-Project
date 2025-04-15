import pygame
from characters.colidable import Colidable
from settings import *

class Particle(Colidable):
    #TO DO
    def __init__(self, path, pos, direction, damage, groups, group):
        super().__init__(path, pos, PARTICLE_SPEED, groups)
        self.direction = direction
        self.group = group
        self.eliminate = False
        self.max_dist = 15*TILESIZE
        self.damage = damage
        
        
    def collision(self, direction, sprite):
        sprite.get_damaged(self.damage)
        self.eliminate = True
    
    def check_kill(self, pos):
        if self.eliminate:
            return True
        
        if ((self.rect.center[0]-pos[0])**2 + (self.rect.center[1]-pos[1])**2)**0.5 > self.max_dist:
            return True
        
        return False
        
    def update(self):
        self.move(self.group)
        