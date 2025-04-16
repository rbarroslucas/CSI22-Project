import pygame

class Weapon:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.weapon_image = pygame.image.load("graphics/arma/arma.png").convert_alpha()