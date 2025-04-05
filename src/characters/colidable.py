import pygame

class Colidable(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        
        self.direction = pygame.math.Vector2()
        self.speed = speed
        
    def move(self, group):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * self.speed
        self.check_collision('horizontal', group)
        
        self.hitbox.y += self.direction.y * self.speed
        self.check_collision('vertical', group)
        
        self.rect.center = self.hitbox.center
        
    def check_collision(self, direction, group):
        if direction == 'horizontal':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)
        
        if direction == 'vertical':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)
        
    def collision(self, direction, sprite):
        pass