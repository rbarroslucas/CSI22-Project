import pygame
import math
from settings import *
from support import import_folder
from characters.entity import Entity

class Enemy(Entity):
    """Classe que representa um inimigo no jogo.

    Herda de Entity. Controla comportamento de movimentação, animação, colisão,
    detecção do jogador e ataque com partículas.
    """

    def __init__(self, name, pos, get_player_pos, get_player_sight, create_particle, groups, obstacle_sprite):
        """Inicializa o inimigo com gráficos, atributos e lógica de perseguição.

        Args:
            name (str): Nome do inimigo, usado para buscar gráficos e sons.
            pos (tuple): Posição inicial do inimigo.
            get_player_pos (Callable): Função para obter a posição atual do jogador.
            get_player_sight (Callable): Função para obter o vetor de visão do jogador.
            create_particle (Callable): Função para instanciar uma partícula.
            groups (list): Lista de grupos de sprites que o inimigo pertence.
            obstacle_sprite (pygame.sprite.Group): Grupo de obstáculos para colisão.
        """
        path = './graphics/' + name + '/stand_front/' + 'stand_front0.png'
        enemy_settings = ENEMY_SETTINGS[name]
        super().__init__(path, pos, create_particle, enemy_settings["speed"], groups, obstacle_sprite)

        self.hitbox = self.rect.inflate(0, -self.rect.height // 2)
        self.particle_path = './graphics/' + name + '/particle'

        # Partículas e cooldowns
        self.casting_cooldown = enemy_settings["casting_cooldown"]

        # Animações
        self.animations = {'stand_front': [], 'stand_back': [], 'stand_right': [], 'stand_left': [],
                           'walk_front': [], 'walk_back': [],  'walk_right': [], 'walk_left': []}
        self.import_assets(name)

        # Raio de ações
        self.attack_radius = enemy_settings["attack_radius"] * TILESIZE
        self.persecute_radius = enemy_settings["persecute_radius"] * TILESIZE
        self.evade_radius = enemy_settings["evade_radius"] * TILESIZE

        # Inteligência artificial
        self.evasion_angle = math.pi / 6
        self.get_player_pos = get_player_pos
        self.get_player_sight = get_player_sight

        # Vida e invencibilidade
        self.health = enemy_settings["health"]
        self.invencible_time = 100
        self.invencible_start = 0

        # Som
        self.attack_sound = pygame.mixer.Sound('./audio/' + name + '.wav')
        self.attack_sound.set_volume(0.6)
        self.sound_cooldown = 4000
        self.sound_start = 0

    def action(self):
        """Define o comportamento do inimigo baseado na posição do jogador.

        Inclui perseguição, evasão e ataque com partículas.
        """
        player_pos = self.get_player_pos()
        player_sight = self.get_player_sight()

        enemy_pos = pygame.math.Vector2(self.rect.center)
        delta = enemy_pos - player_pos

        self.direction = pygame.math.Vector2(0, 0)
        current_time = pygame.time.get_ticks()

        if delta.magnitude() < self.persecute_radius and not self.casting:
            if self.attack_radius > delta.magnitude() > self.evade_radius:
                self.casting = True
                self.casting_start = pygame.time.get_ticks()
                direction = -delta

                if current_time - self.sound_start > self.sound_cooldown:
                    self.attack_sound.play()
                    self.sound_start = current_time

                self.particles.append(self.create_particle('enemy', self.particle_path, self.rect.topleft, direction))

            # Desvio lateral
            direction_perp = pygame.math.Vector2(0, 0)
            alpha = math.atan2(player_sight.y, player_sight.x)
            omega = math.atan2(delta.y, delta.x)

            if alpha <= omega < self.evasion_angle + alpha:
                direction_perp.x += -player_sight.y
                direction_perp.y += player_sight.x
            elif -self.evasion_angle + alpha < omega < alpha:
                direction_perp.x += player_sight.y
                direction_perp.y += -player_sight.x

            # Movimentação básica
            self.direction.x = -1 if delta.x > 0 else (1 if delta.x < 0 else 0)
            self.direction.y = -1 if delta.y > 0 else (1 if delta.y < 0 else 0)

            if delta.magnitude() < self.evade_radius:
                self.direction = -self.direction

            # Ajuste com desvio lateral
            if direction_perp.magnitude() != 0:
                if abs(delta.y) > abs(delta.x):
                    self.direction.x = direction_perp.x
                else:
                    self.direction.y = direction_perp.y

    def animate(self):
        """Atualiza a animação do inimigo com base na direção do movimento."""
        status_aux = 'walk_'

        if self.direction.y < 0:
            status_aux += 'back'
        elif self.direction.y > 0:
            status_aux += 'front'
        elif self.direction.x > 0:
            status_aux += 'right'
        elif self.direction.x < 0:
            status_aux += 'left'

        if status_aux != 'walk_':
            self.status = status_aux
        else:
            self.status = 'stand_' + self.status.split('_')[1]

        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def get_damaged(self, damage):
        """Aplica dano ao inimigo, verificando tempo de invencibilidade.

        Args:
            damage (int): Quantidade de dano a ser aplicada.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.invencible_start > self.invencible_time:
            self.health -= damage
            self.invencible_start = current_time

            if self.health <= 0:
                self.kill()

    def update(self):
        """Atualiza o estado do inimigo a cada frame.

        Inclui lógica de ação, animação, partículas e movimentação.
        """
        self.action()
        self.animate()
        self.cooldown()
        self.update_particles()
        self.move(self.obstacle_sprite)