import pygame

class Colidable(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        
        self.direction = pygame.math.Vector2()
        self.speed = speed
        
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        
    def colision(self):
        pass
        
        