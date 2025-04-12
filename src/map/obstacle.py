import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.rect = surface.get_rect(topleft=pos)
        self.rect = self.rect.inflate(0, +6)
        self.hitbox = self.rect