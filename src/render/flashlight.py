import pygame
import math
from settings import *
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
        brightness = min(2*(i * 255 / layers), 255)
        ring_radius = radius - (radius / layers) * (i + 1)
        ring_sector = create_circle_sector(ring_radius, start_angle, end_angle, 50, max(brightness, BRIGHT_DEFAULT))
        ring_sector.set_alpha(i * 255 / layers)
        surface.blit(ring_sector, (radius - ring_radius, radius - ring_radius))
    return surface

def glow(glow, radius, end):
    layers = 100
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    delta = glow - end
    glow = clamp(glow, 0, 255)
    for i in range(layers):
        k = glow - (delta / layers) * i
        k = clamp(k, 0, 255)
        r = i * (radius)/layers
        pygame.draw.circle(surf, (k, k, k, min(2*k, 255)), surf.get_rect().center, r)
    return surf

class Flashlight(pygame.sprite.Sprite):
    def __init__(self, pos, theta, groups, radius):
        super().__init__(groups)
        self.theta = theta
        self.start_angle = 0
        self.current_angle = 0
        self.radius = radius

        self.original_image = make_rings(self.radius, 100, self.start_angle, theta)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, player_sight):
        angle = math.atan2(player_sight.y, player_sight.x)
        if self.current_angle != angle:
            self.image = make_rings(self.radius, 100, angle, self.theta)
            self.current_angle = angle


