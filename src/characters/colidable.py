import pygame
from settings import *
from abc import ABC, abstractmethod

class Colidable(pygame.sprite.Sprite, ABC):
    def __init__(self, path, pos, speed, groups):
        super().__init__(groups)

        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * SCALE_FACTOR,
                                                         self.image.get_height() * SCALE_FACTOR))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        self.direction = pygame.math.Vector2()
        self.speed = speed

    def move(self, group):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        delta_x = self.direction.x * self.speed
        self.hitbox.x += delta_x
        self.check_collision('horizontal', group)

        delta_y = self.direction.y * self.speed
        self.hitbox.y += delta_y
        self.check_collision('vertical', group)
        
        self.rect.midbottom = self.hitbox.midbottom

    def check_collision(self, direction, group):
        if direction == 'horizontal':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)

        if direction == 'vertical':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)

    @abstractmethod
    def collision(self, direction, sprite):
        pass