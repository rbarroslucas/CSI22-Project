import pygame
from settings import *
from abc import abstractmethod
from characters.colidable import Colidable

class Entity(Colidable):
    def __init__(self, path, pos, speed, groups, obstacle_sprite):
        super().__init__(path, pos, speed, groups)
        
        self.obstacle_sprite = obstacle_sprite
        
    def collision(self, direction, sprite):
        if direction == 'horizontal':
            if self.direction.x>0:
                self.hitbox.right = sprite.hitbox.left
            elif self.direction.x<0:
                self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            if self.direction.y>0:
                self.hitbox.bottom = sprite.hitbox.top
            elif self.direction.y<0:
                self.hitbox.top = sprite.hitbox.bottom
    
    @abstractmethod
    def update(self):
        pass