# interfaces/inventory.py
import pygame
from weapons.inventory_weapon import InventoryWeapon
from items.healing_potion import HealingPotion
from items.strength_potion import StrengthPotion

class Inventory:
    def __init__(self):
        self.weapon = None
        self.items = [None] * 5
        self.slot_size = 64
        self.slot_margin = 8
        self.weapon_margin = 64  # Espaçamento adicional entre arma e itens
        self.font = pygame.font.Font(None, 24)

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

        # Itens (com seleção)
        for i, item in enumerate(self.items):
            x = self.item_start_x + i * (self.slot_size + self.slot_margin)
            rect = pygame.Rect(x, self.y, self.slot_size, self.slot_size)

            pygame.draw.rect(surface, (60, 60, 60), rect)  # Slot normal
            pygame.draw.rect(surface, (30, 30, 30), rect, 3)  # Borda escura

            if item:
                text = self.font.render(str(item), True, (255, 255, 255))
                surface.blit(text, text.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_5:
                index = event.key - pygame.K_1
                self.use_item(index)

    def use_item(self, index):
        item = self.items[index]
        if item:
            print(f"Item usado no slot {index + 1}: {item}")
            # Lógica de uso aqui