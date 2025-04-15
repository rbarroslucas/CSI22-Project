import pygame
import math
from characters.entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self, name, pos, get_player_pos, get_player_sight, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, ENEMY_SPEED, groups, obstacle_sprite)

        self.enemy_surface = pygame.Surface((TILESIZE, TILESIZE))
        self.enemy_surface.fill('blue')
        self.image = self.enemy_surface
        self.rect = self.image.get_rect(topleft=pos)

        ##hard coded, change after
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)

        #animation
        self.status = 'stand_front'
        self.frame_index = 0
        self.animate_speed = 6/FPS
        self.import_enemy_assets(name)

        # ai stuff
        self.evasion_angle = math.pi/3

        self.get_player_pos = get_player_pos
        self.get_player_sight = get_player_sight

    def import_enemy_assets(self, name):
        #TO DO
        pass

    def action(self):
        player_pos = self.get_player_pos()
        player_sight = self.get_player_sight()

        self.direction_perp = pygame.math.Vector2(0, 0)
        self.direction_norm = pygame.math.Vector2(0, 0)

        delta_x = self.rect.center[0] - player_pos[0]
        delta_y = self.rect.center[1] - player_pos[1]

        alpha = math.atan2(player_sight.y, player_sight.x)
        omega = math.atan2(delta_y, delta_x)

        if omega < self.evasion_angle + alpha and omega >= alpha:
            self.direction_perp.x +=  -player_sight.y
            self.direction_perp.y += player_sight.x
        elif omega > -self.evasion_angle + alpha and omega < alpha:
            self.direction_perp.x +=  player_sight.y
            self.direction_perp.y += -player_sight.x

        delta_vector = pygame.math.Vector2(self.rect.center[0] - player_pos[0],
                                     self.rect.center[1] - player_pos[1])
        if delta_vector.length() > 0:
            self.direction_norm = -delta_vector.normalize()
        else:
            self.direction_norm = pygame.math.Vector2(0, 0)

        # Normalize the direction vectors
        if self.direction_perp.magnitude() > 0:
            self.direction_norm = pygame.math.Vector2(0,0)
            self.direction_perp = self.direction_perp.normalize()
        if self.direction_norm.magnitude() > 0:
            self.direction_norm = self.direction_norm.normalize()

        self.direction = self.direction_perp + self.direction_norm



    def animate(self):
        #TO DO
        pass

    def update(self):
        self.action()
        self.move(self.obstacle_sprite)