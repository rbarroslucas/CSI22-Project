import pygame
import math
from settings import *
from support import import_folder
from characters.entity import Entity

class Enemy(Entity):
    def __init__(self, name, pos, get_player_pos, get_player_sight, create_particle, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, create_particle, ENEMY_SPEED, groups, obstacle_sprite)
        ##hard coded, change after
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        self.particle_path = './graphics/' + name + '/particle'
        
        #particles
        self.casting_cooldown = 800
        
        #animation
        self.animations = {'stand_front': [], 'stand_back': [], 'stand_right': [], 'stand_left': [],
                           'walk_front': [], 'walk_back': [],  'walk_right': [], 'walk_left': []}
        self.import_assets(name)

        #radius
        self.attack_radius = 5*TILESIZE
        self.persecute_radius = 7*TILESIZE
        self.evade_radius = 2*TILESIZE        
        
        # ai stuff
        self.evasion_angle = math.pi/6

        self.get_player_pos = get_player_pos
        self.get_player_sight = get_player_sight
        
        self.health = 3
        self.invencible_time = 100
        self.invencible_start = 0

    def action(self):
        player_pos = self.get_player_pos()
        player_sight = self.get_player_sight()

        enemy_pos = pygame.math.Vector2(self.rect.center[0], self.rect.center[1])
        delta = enemy_pos - player_pos
        
        self.direction = pygame.math.Vector2(0, 0)
        
        if delta.magnitude() < self.persecute_radius and not self.casting:
            if delta.magnitude() > self.evade_radius and delta.magnitude() < self.attack_radius:
                self.casting = True
                self.casting_start = pygame.time.get_ticks()
                direction = -delta
                    
                self.particles.append(self.create_particle('enemy', self.particle_path, self.rect.topleft, direction))
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
        status_aux = 'walk_'
        
        if self.direction.y < 0:
            status_aux = status_aux + 'back'
        elif self.direction.y > 0:
            status_aux = status_aux + 'front'
        elif self.direction.x > 0:
            status_aux = status_aux + 'right'
        elif self.direction.x < 0:
            status_aux = status_aux + 'left'
        
        if status_aux != 'walk_':
            self.status = status_aux
        else:
            self.status = 'stand_' + self.status.split('_')[1]
        
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def get_damaged(self, damage):
        current_time = pygame.time.get_ticks()
        if current_time - self.invencible_start > self.invencible_time:
            self.health -= damage
            self.invencible_start = current_time

            if self.health <= 0:
                self.kill()
                
    def update(self):
        self.action()
        self.animate()
        self.cooldown()
        self.update_particles()
        self.move(self.obstacle_sprite)