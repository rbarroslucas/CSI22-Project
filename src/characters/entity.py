import pygame
from settings import *
from abc import ABC, abstractmethod
from colidable import Colidable

class Entity(Colidable, ABC):
    def __init__(self, path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))
        self.rect = self.image.get_rect(topleft=pos)

    @abstractmethod
    def update(self):
        pass