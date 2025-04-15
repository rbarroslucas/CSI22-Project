import pygame
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
        
        self.get_player_pos = get_player_pos
        self.get_player_sight = get_player_sight

    def import_enemy_assets(self, name):
        #TO DO
        pass

    def action(self):
        player_pos = self.get_player_pos()
        player_sight = self.get_player_sight()
        
        delta_x = self.rect.center[0] - player_pos[0]
        delta_y = self.rect.center[1] - player_pos[1]
        
        if delta_x > 0:
            self.direction.x = -1
        elif delta_x < 0:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
        if delta_y > 0:
            self.direction.y = -1
        elif delta_y < 0:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def animate(self):
        #TO DO
        pass

    def update(self):
        self.action()
        self.move(self.obstacle_sprite)