import pygame

class Weapon:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.damage_buff = 0
        self.damage_buff_duration = 0
        self.cooldown_buff = 0
        self.cooldown_buff_duration = 0
        self.weapon_image = pygame.image.load("graphics/arma/arma.png").convert_alpha()