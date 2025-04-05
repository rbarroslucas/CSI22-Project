import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)