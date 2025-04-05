import pygame
from settings import *
from abc import ABC, abstractmethod
from colidable import Colidable

class Entity(Colidable, ABC):
    def __init__(self, path, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    @abstractmethod
    def update(self):
        pass