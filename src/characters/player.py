import pygame
from settings import *
from characters.entity import Entity

class Player(Entity):
    def __init__(self, path, pos, groups):
        super().__init__(path, pos, groups)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * self.speed