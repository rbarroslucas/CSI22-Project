import pygame
from settings import TILESIZE

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, damage, cooldown, pos, groups):
        super().__init__(groups)
        self.name = name
        self.damage = damage
        self.cooldown = cooldown

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill('blue')  # Corrigido: o fill deve vir direto no Surface
        self.rect = self.image.get_rect(topleft=pos)  # Define posição no mapa