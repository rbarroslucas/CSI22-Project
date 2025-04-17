import pygame
from weapons import InventoryWeapon
from items import Potion, DurationPotion
import random


class Inventory:
    """
    Classe que representa o inventário do jogador, contendo armas e itens utilizáveis, como poções.

    O inventário é composto por um slot para arma e múltiplos slots para itens. A classe gerencia a
    exibição dos itens e a troca de armas, além de gerar itens aleatórios que podem ser consumidos pelo jogador.

    Atributos:
        weapon (InventoryWeapon): A arma equipada atualmente no inventário.
        slot_size (int): O tamanho de cada slot de item ou arma (em pixels).
        slot_margin (int): O espaçamento entre os slots de itens.
        weapon_margin (int): O espaçamento adicional entre o slot de arma e os itens.
        font (pygame.font.Font): Fonte usada para desenhar textos no inventário (caso necessário).
        items (list): Lista de itens (poções) no inventário.
        weapon_x (int): Posição horizontal do slot da arma na tela.
        y (int): Posição vertical do inventário na tela.
        item_start_x (int): Posição inicial dos slots de itens, após o slot de arma.

    Métodos:
        __init__: Inicializa o inventário, definindo a arma, os itens e as posições dos slots.
        change_weapon: Troca a arma atual do inventário para a arma fornecida.
        draw: Desenha o inventário na tela, incluindo o slot da arma e os slots dos itens.
        create_items: Cria itens aleatórios (poções) para o inventário, com diferentes buffs e durações.
        load_image: Carrega e escala a imagem de um item (ou poção) para o tamanho do slot.
    """

    def __init__(self):
        """
        Inicializa o inventário, criando a arma e os itens, e definindo as posições dos slots.

        A arma será inicialmente nula e os itens serão gerados aleatoriamente. O inventário será
        posicionado na parte inferior da tela, com os slots de itens dispostos à direita da arma.
        """
        self.weapon = None
        self.slot_size = 64
        self.slot_margin = 8
        self.weapon_margin = 64  # Espaçamento adicional entre arma e itens
        self.font = pygame.font.Font(None, 24)

        # Criação de itens aleatórios
        self.items = self.create_items()

        # Posições dos slots
        screen = pygame.display.get_surface()
        self.weapon_x = screen.get_width() // 2 - (self.slot_size + self.slot_margin) * 3 - self.weapon_margin
        self.y = screen.get_height() - self.slot_size - 20
        self.item_start_x = self.weapon_x + self.slot_size + self.weapon_margin  # Espaçamento maior aqui

    def change_weapon(self, mapWeapon):
        """
        Troca a arma equipada do inventário.

        A arma do inventário é alterada para a nova arma fornecida.

        Parâmetros:
            mapWeapon (Weapon): A nova arma a ser equipada no inventário.
        """
        self.weapon = InventoryWeapon(mapWeapon.name, mapWeapon.damage, mapWeapon.cooldown, self.slot_size)

    def draw(self, surface):
        """
        Desenha o inventário na tela.

        O inventário inclui o slot da arma e os slots dos itens. A arma é desenhada primeiro, seguida pelos itens.
        Cada slot é desenhado como um quadrado, com a imagem do item (se houver) sendo desenhada no centro do slot.

        Parâmetros:
            surface (pygame.Surface): A superfície onde o inventário será desenhado (geralmente a tela).
        """
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
        """
        Cria uma lista de itens aleatórios (poções) para o inventário.

        Os itens gerados incluem poções de cura, poções de dano e poções de cooldown, com diferentes buffs e durações.
        A probabilidade de cada tipo de poção ser gerada é baseada em números aleatórios.

        Retorna:
            list: Lista de objetos de poções, que podem ser instâncias de Potion ou DurationPotion.
        """
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
                items.append(
                    DurationPotion("Damage Potion", buff, duration, self.load_image("graphics/potions/red_potion.png")))
            else:
                if k <= 0.5:
                    buff = 100
                    duration = 10
                else:
                    buff = 200
                    duration = 5
                items.append(DurationPotion("Cooldown Potion", buff, duration,
                                            self.load_image("graphics/potions/blue_potion.png")))
        return items

    def load_image(self, path):
        """
        Carrega uma imagem e a escala para o tamanho adequado do slot.

        Parâmetros:
            path (str): O caminho para a imagem a ser carregada.

        Retorna:
            pygame.Surface: A imagem carregada e escalada para o tamanho do slot.
        """
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (self.slot_size, self.slot_size))