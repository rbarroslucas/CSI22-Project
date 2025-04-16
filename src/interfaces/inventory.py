# interfaces/inventory.py
import pygame
from weapons.inventory_weapon import InventoryWeapon
from items.potion import Potion
from items.durantion_potion import DurationPotion
import random

class Inventory:
    def __init__(self):
        self.weapon = None
        self.slot_size = 64
        self.slot_margin = 8
        self.weapon_margin = 64  # Espaçamento adicional entre arma e itens
        self.font = pygame.font.Font(None, 24)

        # Create Items Randomly
        self.items = self.create_items()

        # Posição dos slots
        screen = pygame.display.get_surface()
        self.weapon_x = screen.get_width() // 2 - (self.slot_size + self.slot_margin) * 3 - self.weapon_margin
        self.y = screen.get_height() - self.slot_size - 20
        self.item_start_x = self.weapon_x + self.slot_size + self.weapon_margin  # Espaçamento maior aqui

    def change_weapon(self, mapWeapon):
        self.weapon = InventoryWeapon(mapWeapon.name, mapWeapon.damage, mapWeapon.cooldown, self.slot_size)

    def draw(self, surface):
        weapon_rect = pygame.Rect(self.weapon_x, self.y, self.slot_size, self.slot_size)
        pygame.draw.rect(surface, (60, 60, 60), weapon_rect)
        pygame.draw.rect(surface, (30, 30, 30), weapon_rect, 3)

        if self.weapon:
            image_rect = self.weapon.image.get_rect(center=weapon_rect.center)
            surface.blit(self.weapon.image, image_rect)

        for i, item in enumerate(self.items):
            x = self.item_start_x + i * (self.slot_size + self.slot_margin)
            item_rect = pygame.Rect(x, self.y, self.slot_size, self.slot_size)

            pygame.draw.rect(surface, (60, 60, 60), item_rect)  # Slot normal
            pygame.draw.rect(surface, (30, 30, 30), item_rect, 3)  # Borda escura

            if item:
                image_rect = item.image.get_rect(center=item_rect.center)
                surface.blit(item.image, image_rect)

    def create_items(self):
        items = []
        for i in range(3):
            j = random.random()
            k = random.random()
            if j <= 0.4:
                if k <= 0.9:
                    buff = 1
                else:
                    buff = 2
                items.append(Potion("Healing Potion", buff, self.load_image("graphics/potions/green_potion.png")))
            elif j <= 0.8:
                if k <= 0.7:
                    buff = 1
                    duration = 4
                else:
                    buff = 2
                    duration = 3
                items.append(DurationPotion("Damage Potion", buff, duration, self.load_image("graphics/potions/red_potion.png")))
            else:
                if k <= 0.5:
                    buff = 100
                    duration = 10
                else:
                    buff = 200
                    duration = 5
                items.append(DurationPotion("Cooldown Potion", buff, duration, self.load_image("graphics/potions/blue_potion.png")))
        return items

    def load_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (self.slot_size, self.slot_size))