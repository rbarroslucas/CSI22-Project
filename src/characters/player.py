import pygame
from settings import *
from characters.entity import Entity

class Player(Entity):
    def __init__(self, path, pos, groups):
        super().__init__(path, pos, groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        pass