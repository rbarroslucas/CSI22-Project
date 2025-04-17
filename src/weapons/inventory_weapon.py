import pygame
from weapons.weapon import Weapon


class InventoryWeapon(Weapon):
    """
    Classe que representa uma arma no inventário do jogador, estendendo a classe `Weapon`.
    A arma tem uma imagem redimensionada conforme o tamanho do slot no inventário.

    Atributos:
        name (str): Nome da arma.
        damage (int): Dano da arma.
        cooldown (int): Tempo de recarga da arma.
        image (pygame.Surface): Imagem da arma redimensionada conforme o tamanho do slot no inventário.
    """

    def __init__(self, name, damage, cooldown, slot_size):
        """
        Inicializa uma nova arma no inventário.

        Parâmetros:
            name (str): Nome da arma.
            damage (int): Dano da arma.
            cooldown (int): Tempo de recarga da arma.
            slot_size (int): Tamanho do slot no inventário para o qual a imagem da arma será redimensionada.
        """
        super().__init__(name, damage, cooldown)
        self.image = pygame.transform.scale(self.weapon_image, (slot_size, slot_size))