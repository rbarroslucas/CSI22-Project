import pygame
from settings import *
from support import import_folder
from characters.colidable import Colidable

class Player(Colidable):
    def __init__(self, name, pos, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, PLAYER_SPEED, groups)
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        self.status = 'stand_front'
        self.import_player_assets(name)
        
    def import_player_assets(self, name):
        character_path = './graphics/' + name + '/'
        self.animations = {'stand_front': [], 'stand_frontright': [], 'stand_frontleft': [], 
                           'stand_back': [], 'stand_backright': [], 'stand_backleft': [],
                           'stand_right': [], 'stand_left': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def collision(self, direction, sprite):
        if direction == 'horizontal':
            if self.direction.x>0:
                self.hitbox.right = sprite.hitbox.left
            elif self.direction.x<0:
                self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            if self.direction.y>0:
                self.hitbox.bottom = sprite.hitbox.top
            elif self.direction.y<0:
                self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        status_aux = 'stand_'
        
        if self.direction.y < 0:
            status_aux = status_aux + 'back'
        elif self.direction.y > 0:
            status_aux = status_aux + 'front'
            
        if self.direction.x > 0:
            status_aux = status_aux + 'right'
        elif self.direction.x < 0:
            status_aux = status_aux + 'left'
        
        if status_aux != 'stand_':
            self.status = status_aux
        
        self.image = self.animations[self.status][0]
    
    def update(self):
        self.input()
        self.animate()
        self.move(self.obstacle_sprite)