import pygame
from settings import *
from abc import ABC, abstractmethod

class Entity(pygame.sprite.Sprite, ABC):
    def __init__(self, path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    @abstractmethod
    def update(self):
        pass