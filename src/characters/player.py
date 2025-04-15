import pygame
from settings import *
from characters.entity import Entity

class Player(Entity):
    def __init__(self, name, pos, switch_player, drag_ghost, create_particle, groups, obstacle_sprite):
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        super().__init__(path, pos, create_particle, PLAYER_SPEED, groups, obstacle_sprite)
        ##hard coded, change after
        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)

        #particles
        self.casting_cooldown = 400

        #animation
        self.animations = {'stand_front': [], 'stand_frontright': [], 'stand_frontleft': [], 'stand_back': [], 'stand_backright': [], 'stand_backleft': [], 'stand_right': [], 'stand_left': [],
                           'walk_front': [], 'walk_frontright': [], 'walk_frontleft': [], 'walk_back': [], 'walk_backright': [], 'walk_backleft': [], 'walk_right': [], 'walk_left': []}
        self.import_assets(name)

        self.active = False
        self.switch_player = switch_player
        self.switch_cooldown = 400
        self.switch_start = 0

        self.drag_ghost = drag_ghost
        self.drag_cooldown = 400
        self.drag_start = 0
        
        self.health = 3
        self.invencible_time = 100
        self.invencible_start = 0

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
                direction = self.sight()

                self.particles.append(self.create_particle('player', self.rect.topleft, direction))

            current_time = pygame.time.get_ticks()

            if keys[pygame.K_k]:
                if current_time - self.drag_start > self.drag_cooldown:
                    self.drag_start = current_time
                    self.drag_ghost()

            if keys[pygame.K_SPACE]:
                if current_time - self.switch_start >= self.switch_cooldown:
                    self.switch_start = current_time
                    self.switch_player()

    def sight(self):
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

        return direction

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

    def set_transparency(self, alpha):
        if self.image:
            self.image.set_alpha(alpha)

    def change_active(self, bool):
        self.active = bool

    def teleport_ghost(self, pos):
        self.rect.center = pos
        self.hitbox = self.rect

    def get_rect_center(self):
        return self.rect.center

    def get_damaged(self, damage):
        current_time = pygame.time.get_ticks()
        if current_time - self.invencible_start > self.invencible_time:
            self.health -= damage
            self.invencible_start = current_time
            
            if self.health <= 0:
                self.switch_player()
                
    def check_death(self):
        return self.health <= 0
    
    def update(self):
        if self.active:
            self.input()
            self.cooldown()
            self.animate()
            self.update_particles()
            self.move(self.obstacle_sprite)