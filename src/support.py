from os import walk
from settings import *
import pygame

def import_folder(path):
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
    """Clamp value between mini and maxi"""
    if value < mini:
        return mini
    elif maxi < value:
        return maxi
    else:
        return value