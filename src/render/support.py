from csv import reader
import pygame

def import_csv_layout(path):
    """
    Importa o layout de um arquivo CSV e converte em uma lista de listas que representa o mapa de terreno.

    Parâmetros:
        path (str): Caminho para o arquivo CSV que contém o layout do nível.

    Retorna:
        list: Uma lista de listas representando o layout do mapa de terreno, onde cada elemento
              é um valor do CSV (por exemplo, um número ou uma string que representa o tipo de terreno).
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))

    return terrain_map

def blur_surface(surface, scale_factor=0.25):
    """
    Aplica um desfoque na superfície fornecida, redimensionando-a para um tamanho menor e depois escalando de volta ao tamanho original.

    Parâmetros:
        surface (pygame.Surface): A superfície para a qual o desfoque será aplicado.
        scale_factor (float): Fator de escala usado para reduzir o tamanho da superfície antes de redimensioná-la de volta.
                              O valor padrão é 0.25 (25%).

    Retorna:
        pygame.Surface: A superfície com o desfoque aplicado.
    """
    small = pygame.transform.smoothscale(surface, (int(surface.get_width() * scale_factor),
                                                   int(surface.get_height() * scale_factor)))
    return pygame.transform.smoothscale(small, surface.get_size())