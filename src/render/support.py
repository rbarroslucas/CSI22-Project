from csv import reader

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))

    return terrain_map

def blur_surface(surface, scale_factor=0.25):
    small = pygame.transform.smoothscale(surface, (int(surface.get_width() * scale_factor),
                                                   int(surface.get_height() * scale_factor)))
    return pygame.transform.smoothscale(small, surface.get_size())