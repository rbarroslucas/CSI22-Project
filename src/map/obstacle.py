import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    """
    Classe que representa um obstáculo no jogo. Os obstáculos são entidades que podem ser
    adicionadas ao grupo de sprites do jogo e interagir com outros objetos. Cada obstáculo
    possui uma posição, um retângulo delimitador e uma hitbox.

    Atributos:
        rect (pygame.Rect): O retângulo que representa a área do obstáculo, com base na
                            superfície fornecida e a posição inicial.
        hitbox (pygame.Rect): A hitbox do obstáculo, usada para detectar colisões.

    Métodos:
        __init__: Inicializa o obstáculo com uma posição, superfície e grupos.
    """

    def __init__(self, pos, surface, groups):
        """
        Inicializa o obstáculo com a posição, a superfície e os grupos fornecidos.

        Parâmetros:
            pos (tuple): A posição inicial do obstáculo (x, y).
            surface (pygame.Surface): A superfície que será usada para determinar o tamanho
                                      e o retângulo do obstáculo.
            groups (list): Lista de grupos aos quais o obstáculo será adicionado.
        """
        super().__init__(groups)
        self.rect = surface.get_rect(topleft=pos)  # Define o retângulo com base na posição
        self.rect = self.rect.inflate(0, +6)  # Expande o retângulo verticalmente
        self.hitbox = self.rect  # Define a hitbox como o retângulo ajustado