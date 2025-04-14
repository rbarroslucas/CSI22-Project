import pygame
from characters.entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, ENEMY_SPEED, groups, obstacle_sprite)
        
        ##hard coded, change after
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        
        #animation
        self.status = 'stand_front'
        self.frame_index = 0
        self.animate_speed = 6/FPS
        self.import_enemy_assets(name)
        
    def import_enemy_assets(self, name):
        #TO DO
        pass

    def action(self):
        #TO DO
        pass

    def animate(self):
        #TO DO
        pass