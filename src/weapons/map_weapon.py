import pygame
from weapons.weapon import Weapon
from settings import TILESIZE

class MapWeapon(Weapon, pygame.sprite.Sprite):
    """
    Classe que representa uma arma no mapa, herdando de `Weapon` e `pygame.sprite.Sprite`.
    A arma pode ser colocada no mapa, ter uma imagem e ser interagida pelo jogador.

    Atributos:
        name (str): Nome da arma.
        damage (int): Dano da arma.
        cooldown (int): Tempo de recarga da arma.
        image (pygame.Surface): Imagem da arma.
        rect (pygame.Rect): Retângulo de colisão da arma.
    """

    def __init__(self, name, damage, cooldown, pos, groups):
        """
        Inicializa uma nova arma no mapa.

        Parâmetros:
            name (str): Nome da arma.
            damage (int): Dano da arma.
            cooldown (int): Tempo de recarga da arma.
            pos (tuple): Posição inicial da arma no mapa (x, y).
            groups (list): Lista de grupos de sprites aos quais a arma será adicionada.
        """
        Weapon.__init__(self, name, damage, cooldown)
        pygame.sprite.Sprite.__init__(self, groups)

        # Carrega e redimensiona a imagem da arma
        self.image = pygame.image.load("graphics/arma/arma.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
