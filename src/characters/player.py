import pygame
from settings import *
from support import import_folder
from characters.entity import Entity
from characters.particle import Particle

class Player(Entity):
    def __init__(self, name, pos, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, PLAYER_SPEED, groups, obstacle_sprite)
        self.g = groups
        ##hard coded, change after
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        
        #particles
        self.particles = []
        self.casting = False
        self.casting_start = 0
        self.casting_cooldown = 400
        
        #animation
        self.status = 'stand_front'
        self.frame_index = 0
        self.animate_speed = 6/FPS
        self.import_player_assets(name)
        
    def import_player_assets(self, name):
        character_path = './graphics/' + name + '/'
        self.animations = {'stand_front': [], 'stand_frontright': [], 'stand_frontleft': [], 'stand_back': [], 'stand_backright': [], 'stand_backleft': [], 'stand_right': [], 'stand_left': [],
                           'walk_front': [], 'walk_frontright': [], 'walk_frontleft': [], 'walk_back': [], 'walk_backright': [], 'walk_backleft': [], 'walk_right': [], 'walk_left': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.casting:
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

            if keys[pygame.K_j]:
                self.direction.x = 0
                self.direction.y = 0
                
                self.casting = True
                self.casting_start = pygame.time.get_ticks()
                direction = pygame.math.Vector2()
                
                status = self.status.split('_')
                
                if 'front' in status[1]:
                    direction.y = 1
                elif 'back' in status[1]:
                    direction.y = -1
                else:
                    direction.y = 0
                    
                if 'right' in status[1]:
                    direction.x = 1
                elif 'left' in status[1]:
                    direction.x = -1
                else:
                    direction.x = 0
                    
                self.particles.append(Particle(self.rect.topleft, direction, self.g, self.obstacle_sprite))

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        
        if self.casting:
            if current_time - self.casting_start >= self.casting_cooldown:
                self.casting = False
    
    def animate(self):
        status_aux = 'walk_'
        
        if self.direction.y < 0:
            status_aux = status_aux + 'back'
        elif self.direction.y > 0:
            status_aux = status_aux + 'front'
            
        if self.direction.x > 0:
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
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.eliminate:
                self.particles.remove(particle)
                particle.kill()
    
    def update(self):
        self.input()
        self.cooldown()
        self.animate()
        self.update_particles()
        self.move(self.obstacle_sprite)