import pygame
from settings import *
from abc import ABC, abstractmethod

class Colidable(pygame.sprite.Sprite, ABC):
    """Classe abstrata base para sprites colidíveis no jogo.

    Herda de pygame.sprite.Sprite e ABC para permitir herança múltipla e métodos abstratos.
    """

    def __init__(self, path, pos, speed, groups):
        """Inicializa o objeto Colidable.

        Args:
            path (str): Caminho da imagem do sprite.
            pos (tuple): Posição inicial (x, y).
            speed (float): Velocidade de movimento.
            groups (list): Lista de grupos de sprites aos quais o objeto pertence.
        """
        super().__init__(groups)

        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (self.image.get_width() * SCALE_FACTOR, self.image.get_height() * SCALE_FACTOR)
        )
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        self.direction = pygame.math.Vector2()
        self.speed = speed

    def move(self, group):
        """Move o sprite com base na direção e velocidade, tratando colisões.

        Args:
            group (pygame.sprite.Group): Grupo de sprites com os quais verificar colisão.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        delta_x = self.direction.x * self.speed
        self.hitbox.x += delta_x
        self.check_collision('horizontal', group)

        delta_y = self.direction.y * self.speed
        self.hitbox.y += delta_y
        self.check_collision('vertical', group)

        self.rect.midbottom = self.hitbox.midbottom

    def check_collision(self, direction, group):
        """Verifica e trata colisões com outros sprites no grupo.

        Args:
            direction (str): Direção do movimento, 'horizontal' ou 'vertical'.
            group (pygame.sprite.Group): Grupo de sprites para verificar colisão.
        """
        if direction == 'horizontal':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)

        if direction == 'vertical':
            for sprite in group:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.collision(direction, sprite)

    @abstractmethod
    def collision(self, direction, sprite):
        """Metodo abstrato a ser implementado para tratar colisões.

        Args:
            direction (str): Direção da colisão ('horizontal' ou 'vertical').
            sprite (pygame.sprite.Sprite): Sprite com o qual houve a colisão.
        """
        pass
