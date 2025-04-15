import pygame
import math
from support import clamp

def create_circle_sector(radius, start_angle, end_angle, segments=50):
    size = (radius * 2, radius * 2)
    surface = pygame.Surface(size, pygame.SRCALPHA)

    center = (radius, radius)

    points = [center]

    for i in range(segments + 1):
        angle_segment = start_angle + (end_angle - start_angle) * (i / segments)
        x = center[0] + radius * math.cos(angle_segment)
        y = center[1] + radius * math.sin(angle_segment)
        points.append((x, y))

    pygame.draw.polygon(surface, [255, 255, 255], points)

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
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.original_image = surface
        self.image = surface
        self.theta = math.pi/6
        self.start_angle = self.theta
        self.current_angle = self.start_angle
        self.rect = self.image.get_rect(topleft=pos)
        self.alpha = 255
        self.fade_speed = 5

    def update(self, player_sight):
        angle = math.atan2(player_sight.y, player_sight.x)
        if self.current_angle != angle:
            self.start_angle = angle - self.theta / 2
            self.end_angle = angle + self.theta / 2
            self.image = create_circle_sector(1000, self.start_angle, self.end_angle)
            self.current_angle = angle


