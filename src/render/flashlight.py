import pygame
import math
from settings import *
from support import clamp

def create_circle_sector(radius, start_angle, end_angle, segments=50, brightness=255):
    """
    Cria um setor circular com base nos parâmetros fornecidos.

    Este metodo desenha um setor circular (parte de um círculo) com um raio específico, ângulos de início e fim,
    e um número definido de segmentos para aproximar a curva. A cor do setor é definida pela variável de brilho.

    Parâmetros:
        radius (int): O raio do círculo.
        start_angle (float): O ângulo de início do setor em radianos.
        end_angle (float): O ângulo de fim do setor em radianos.
        segments (int): O número de segmentos para aproximar o arco (quanto maior, mais suave o arco).
        brightness (int): O brilho da cor do setor (0-255).

    Retorna:
        pygame.Surface: Superfície contendo o setor circular desenhado.
    """
    size = (radius * 2, radius * 2)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (radius, radius)
    points = [center]

    for i in range(segments + 1):
        angle_segment = start_angle + (end_angle - start_angle) * (i / segments)
        x = center[0] + radius * math.cos(angle_segment)
        y = center[1] + radius * math.sin(angle_segment)
        points.append((x, y))

    pygame.draw.polygon(surface, [brightness, brightness, brightness], points)
    return surface

def make_rings(radius, layers, angle, theta):
    """
    Cria anéis concêntricos em torno de um ponto central, com opacidade variável e brilho ajustado por camada.

    Este metodo cria uma série de anéis concêntricos desenhados sobre uma superfície, com a opacidade e brilho
    de cada anel dependendo da camada em que se encontra. O ângulo e o comprimento do arco do setor de cada anel
    também são ajustáveis.

    Parâmetros:
        radius (int): O raio máximo dos anéis.
        layers (int): O número de camadas (anéis) a serem desenhadas.
        angle (float): O ângulo central do arco dos anéis.
        theta (float): O ângulo do arco do setor.

    Retorna:
        pygame.Surface: Superfície contendo os anéis desenhados.
    """
    size = (radius * 2, radius * 2)
    surface = pygame.Surface(size, pygame.SRCALPHA)
    start_angle = angle - (theta / 2)
    end_angle = angle + (theta / 2)
    for i in range(layers):
        brightness = max(min((i * 255 / layers), 255), 100)
        ring_radius = radius - (radius / layers) * (i + 1)
        ring_sector = create_circle_sector(ring_radius, start_angle, end_angle, 50, brightness)
        if brightness < 140:
            alpha = 0
        else:
            alpha = i * 255 / layers
        ring_sector.set_alpha(alpha)
        surface.blit(ring_sector, (radius - ring_radius, radius - ring_radius))
    return surface

def glow(glow, radius, end):
    """
    Cria um efeito de brilho que se dissipa de forma radial.

    Este metodo cria um efeito de brilho com base no parâmetro `glow`, que é o nível de brilho central,
    dissipando-se até o parâmetro `end` em uma superfície circular. O brilho diminui conforme se afasta do centro.

    Parâmetros:
        glow (int): O valor de brilho central (0-255).
        radius (int): O raio do efeito de brilho.
        end (int): O valor de brilho na borda do efeito (0-255).

    Retorna:
        pygame.Surface: Superfície contendo o efeito de brilho desenhado.
    """
    layers = 100
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    delta = glow - end
    glow = clamp(glow, 0, 255)
    for i in reversed(range(layers)):
        k = glow - (delta / layers) * i
        k = clamp(k, 0, 255)
        r = i * (radius) / layers
        pygame.draw.circle(surf, (k, k, k, min(2 * k, 255)), surf.get_rect().center, r)
    return surf

class Flashlight(pygame.sprite.Sprite):
    """
    Classe que representa uma lanterna (flashlight) com um efeito de brilho circular.

    A lanterna projeta um feixe de luz com a forma de um anel, e sua direção pode ser alterada com base na
    posição do jogador. A lanterna também pode exibir o efeito de iluminação de forma dinâmica.

    Atributos:
        theta (float): O ângulo do feixe de luz da lanterna.
        radius (int): O raio do feixe de luz da lanterna.
        original_image (pygame.Surface): A imagem original da lanterna, com o efeito de brilho.
        image (pygame.Surface): A imagem atual da lanterna, que pode ser atualizada com base na posição.
        rect (pygame.Rect): O retângulo que define a posição e tamanho da lanterna.

    Métodos:
        __init__: Inicializa a lanterna com base no posicionamento e configurações.
        update: Atualiza a imagem da lanterna com base na direção do jogador.
    """

    def __init__(self, pos, theta, groups, radius):
        """
        Inicializa a lanterna com a posição, ângulo, grupos de sprites e raio fornecidos.

        Parâmetros:
            pos (tuple): A posição inicial da lanterna na tela (x, y).
            theta (float): O ângulo do feixe de luz.
            groups (pygame.sprite.Group): Os grupos aos quais a lanterna pertence.
            radius (int): O raio da área iluminada pela lanterna.
        """
        super().__init__(groups)
        self.theta = theta
        self.start_angle = 0
        self.current_angle = 0
        self.radius = radius

        # Gera a imagem da lanterna
        self.original_image = make_rings(self.radius, 15, self.start_angle, theta)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, player_sight):
        """
        Atualiza a direção da lanterna com base na posição do jogador.

        A lanterna se orienta para o jogador, ajustando o ângulo de seu feixe de luz.

        Parâmetros:
            player_sight (pygame.math.Vector2): A posição do jogador, usada para calcular a direção do feixe de luz.
        """
        angle = math.atan2(player_sight.y, player_sight.x)
        if self.current_angle != angle:
            self.image = make_rings(self.radius, 15, angle, self.theta)
            self.current_angle = angle