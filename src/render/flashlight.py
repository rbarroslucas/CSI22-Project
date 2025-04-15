import pygame
import math
from support import clamp

def create_circle_sector(radius, start_angle, end_angle, segments=50, brightness = 255):
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
        size = (radius * 2, radius * 2)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        start_angle = angle - (theta / 2)
        end_angle = angle + (theta / 2)
        for i in range(layers):
            brightness = (i * 255 // layers)
            ring_radius = radius - (radius // layers) * (i + 1)
            ring_sector = create_circle_sector(ring_radius, start_angle, end_angle, 50, brightness)
            surface.blit(ring_sector, (radius - ring_radius, radius - ring_radius))
        return surface

def glow(glow, radius, layers):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    glow = clamp(glow, 0, 255)
    for i in range(layers):
        k = i * glow
        k = clamp(k, 0, 255)
        pygame.draw.circle(surf, (k, k, k), surf.get_rect().center, radius - i * 3)

    return surf

class Flashlight(pygame.sprite.Sprite):
    def __init__(self, pos, theta, groups, radius):
        super().__init__(groups)
        self.theta = theta
        self.start_angle = 0
        self.current_angle = 0
        self.radius = radius

        self.original_image = make_rings(self.radius, 50, self.start_angle, theta)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, player_sight):
        angle = math.atan2(player_sight.y, player_sight.x)
        if self.current_angle != angle:
            self.image = make_rings(self.radius, 20, angle, self.theta)
            self.current_angle = angle


