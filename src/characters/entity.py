import pygame
from settings import *
from abc import abstractmethod
from support import import_folder
from characters.colidable import Colidable

class Entity(Colidable):
    def __init__(self, path, pos, create_particle, speed, groups, obstacle_sprite):
        super().__init__(path, pos, speed, groups)
        
        self.obstacle_sprite = obstacle_sprite
        
        #particles
        self.create_particle = create_particle
        self.particles = []
        self.casting = False
        self.casting_start = 0
        
        #animation
        self.status = 'stand_front'
        self.frame_index = 0
        self.animate_speed = 6/FPS
    
    def import_assets(self, name):
        character_path = './graphics/' + name + '/'
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
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
    
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        
        if self.casting:
            if current_time - self.casting_start >= self.casting_cooldown:
                self.casting = False
                
    def update_particles(self):
        for particle in self.particles[:]:
            eliminate = particle.check_kill(self.rect.center)
            if eliminate:
                self.particles.remove(particle)
                particle.kill()
    
    @abstractmethod
    def animate(self):
        pass
    
    @abstractmethod
    def get_damaged(self, damage):
        pass
    
    @abstractmethod
    def update(self):
        pass