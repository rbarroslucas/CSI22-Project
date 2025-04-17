from os import walk
from settings import *
import pygame


def import_folder(path):
    """
    Carrega todas as imagens de uma pasta e as escala.

    Args:
        path (str): O caminho para a pasta onde as imagens estão localizadas.

    Returns:
        list: Uma lista contendo as superfícies (imagens) carregadas e escaladas.
    """
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            fullpath = path + '/' + image
            image_surf = pygame.image.load(fullpath).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * SCALE_FACTOR,
                                                             image_surf.get_height() * SCALE_FACTOR))
            surface_list.append(image_surf)

    return surface_list


def clamp(value, mini, maxi):
    """
    Limita o valor fornecido entre um mínimo e um máximo.

    Args:
        value (int/float): O valor que será limitado.
        mini (int/float): O valor mínimo.
        maxi (int/float): O valor máximo.

    Returns:
        int/float: O valor limitado entre mini e maxi.
    """
    if value < mini:
        return mini
    elif maxi < value:
        return maxi
    else:
        return value


def blur_surface(surface, scale_factor=0.25):
    """
    Aplica um efeito de desfoque na superfície fornecida.

    A função redimensiona a superfície para um tamanho menor e depois a redimensiona
    novamente para o tamanho original, criando um efeito de desfoque.

    Args:
        surface (pygame.Surface): A superfície a ser desfocada.
        scale_factor (float): Fator de escala para reduzir o tamanho da superfície antes de redimensioná-la de volta.

    Returns:
        pygame.Surface: A superfície com o efeito de desfoque aplicado.
    """
    small = pygame.transform.smoothscale(surface, (int(surface.get_width() * scale_factor),
                                                   int(surface.get_height() * scale_factor)))
    return pygame.transform.smoothscale(small, surface.get_size())