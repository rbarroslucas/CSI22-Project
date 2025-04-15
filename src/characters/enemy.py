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

        #radius
        
        self.attack_radius = 5*TILESIZE
        self.persecute_radius = 7*TILESIZE
        self.evade_radius = 2*TILESIZE        
        
        # ai stuff
        self.evasion_angle = math.pi/6

        self.get_player_pos = get_player_pos
        self.get_player_sight = get_player_sight

    def import_enemy_assets(self, name):
        #TO DO
        pass

    def action(self):
        player_pos = self.get_player_pos()
        player_sight = self.get_player_sight()

        enemy_pos = pygame.math.Vector2(self.rect.center[0], self.rect.center[1])
        delta = enemy_pos - player_pos
        
        self.direction = pygame.math.Vector2(0, 0)
        
        if delta.magnitude() < self.persecute_radius:
            direction_perp = pygame.math.Vector2(0, 0)

            alpha = math.atan2(player_sight.y, player_sight.x)
            omega = math.atan2(delta.y, delta.x)

            if omega < self.evasion_angle + alpha and omega >= alpha:
                direction_perp.x +=  -player_sight.y
                direction_perp.y += player_sight.x
            elif omega > -self.evasion_angle + alpha and omega < alpha:
                direction_perp.x +=  player_sight.y
                direction_perp.y += -player_sight.x

            if delta.x > 0:
                self.direction.x = -1
            elif delta.x < 0:
                self.direction.x = 1
            else:
                self.direction.x = 0

            if delta.y > 0:
                self.direction.y = -1
            elif delta.y < 0:
                self.direction.y = 1
            else:
                self.direction.y = 0

            if delta.magnitude() < self.evade_radius:
                self.direction = -self.direction
            
            if direction_perp.magnitude() != 0:
                if(abs(delta.y) > abs(delta.x)):
                    self.direction.x = direction_perp.x
                else:
                    self.direction.y = direction_perp.y

    def animate(self):
        #TO DO
        pass

    def update(self):
        self.action()
        self.move(self.obstacle_sprite)