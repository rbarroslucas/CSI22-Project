import pygame
from characters.colidable import Colidable
from settings import *

class Particle(Colidable):
    #TO DO
    def __init__(self, pos, direction, groups, group):
        super().__init__('./graphics/1.png', pos, PARTICLE_SPEED, groups)
        self.direction = direction
        self.group = group
        self.eliminate = False
        
    def collision(self, direction, sprite):
        self.eliminate = True
        
    def update(self):
        self.move(self.group)