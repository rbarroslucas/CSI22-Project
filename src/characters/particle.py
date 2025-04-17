import pygame
from characters.colidable import Colidable
from settings import *
from support import import_folder


class Particle(Colidable):
    """
    Representa uma partícula projetada (como uma magia ou projétil) que se move em uma direção,
    aplica dano em colisões e desaparece após certa distância ou impacto.

    Args:
        path (str): Caminho para a pasta contendo as imagens da animação da partícula.
        pos (tuple): Posição inicial da partícula.
        direction (pygame.math.Vector2): Direção de movimento da partícula.
        damage (int): Dano causado pela partícula ao colidir com um alvo.
        groups (list): Lista de grupos do Pygame aos quais a partícula pertence.
        group (pygame.sprite.Group): Grupo de sprites com os quais a partícula pode colidir.
    """

    def __init__(self, path, pos, direction, damage, groups, group):
        super().__init__(path + '/particle0.png', pos, PARTICLE_SPEED, groups)
        self.direction = direction
        self.group = group
        self.eliminate = False
        self.max_dist = 15 * TILESIZE
        self.damage = damage
        self.frame_index = 0
        self.animate_speed = 6 / FPS
        self.animation = import_folder(path)
        self.hitbox = self.rect.inflate(-self.rect.width // 2, -self.rect.height // 2)

    def collision(self, direction, sprite):
        """
        Aplica dano ao sprite colidido e marca a partícula para remoção.

        Args:
            direction (str): Direção da colisão ('horizontal' ou 'vertical'), não usada aqui.
            sprite (pygame.sprite.Sprite): Sprite com o qual a partícula colidiu.
        """
        sprite.get_damaged(self.damage)
        self.eliminate = True

    def check_kill(self, pos):
        """
        Verifica se a partícula deve ser eliminada, seja por colisão ou por ter percorrido distância máxima.

        Args:
            pos (tuple): Posição de referência para calcular a distância percorrida pela partícula.

        Returns:
            bool: True se a partícula deve ser removida, False caso contrário.
        """
        if self.eliminate:
            return True

        distance = ((self.rect.center[0] - pos[0]) ** 2 + (self.rect.center[1] - pos[1]) ** 2) ** 0.5
        if distance > self.max_dist:
            return True

        return False

    def animate(self):
        """
        Atualiza a animação da partícula com base na velocidade de animação.
        """
        self.frame_index += self.animate_speed
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]

    def update(self):
        """
        Atualiza a partícula a cada frame, incluindo animação e movimentação com verificação de colisão.
        """
        self.animate()
        self.move(self.group)