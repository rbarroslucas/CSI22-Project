import pygame
from weapons.weapon import Weapon

class InventoryWeapon(Weapon):
    def __init__(self, name, damage, cooldown, slot_size):
        super().__init__(name, damage, cooldown)
        self.image = pygame.transform.scale(self.weapon_image, (slot_size, slot_size))