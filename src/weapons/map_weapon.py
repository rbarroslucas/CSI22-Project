import pygame
from weapons.weapon import Weapon
from settings import TILESIZE

class MapWeapon(Weapon, pygame.sprite.Sprite):
    def __init__(self, name, damage, cooldown, pos, groups):
        Weapon.__init__(self, name, damage, cooldown)
        pygame.sprite.Sprite.__init__(self, groups)

        self.image = pygame.image.load("graphics/arma/arma.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)