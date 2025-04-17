import pygame
from settings import *
from abc import abstractmethod
from support import import_folder
from characters.colidable import Colidable


class Entity(Colidable):
    """
    Classe base abstrata para entidades animadas no jogo, que possuem colisão, partículas,
    e podem ser estendidas por personagens jogáveis ou inimigos.

    Args:
        path (str): Caminho para o sprite inicial da entidade.
        pos (tuple): Posição inicial da entidade no mapa.
        create_particle (Callable): Função responsável por gerar partículas visuais.
        speed (float): Velocidade de movimento da entidade.
        groups (list): Lista de grupos do pygame aos quais a entidade pertence.
        obstacle_sprite (pygame.sprite.Group): Grupo de sprites que representam obstáculos.
    """

    def __init__(self, path, pos, create_particle, speed, groups, obstacle_sprite):
        super().__init__(path, pos, speed, groups)

        self.obstacle_sprite = obstacle_sprite

        # Partículas
        self.create_particle = create_particle
        self.particles = []
        self.casting = False
        self.casting_start = 0

        # Animação
        self.status = 'stand_front'
        self.frame_index = 0
        self.animate_speed = 6 / FPS

    def import_assets(self, name):
        """
        Importa as animações da entidade com base no nome fornecido.

        Args:
            name (str): Nome da entidade (normalmente o nome da pasta com os sprites).
        """
        character_path = './graphics/' + name + '/'

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def collision(self, direction, sprite):
        """
        Ajusta a posição da entidade para evitar sobreposição com outro sprite durante colisões.

        Args:
            direction (str): Direção da colisão ('horizontal' ou 'vertical').
            sprite (pygame.sprite.Sprite): Sprite com o qual houve a colisão.
        """
        if direction == 'horizontal':
            if self.direction.x > 0:
                self.hitbox.right = sprite.hitbox.left
            elif self.direction.x < 0:
                self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            if self.direction.y > 0:
                self.hitbox.bottom = sprite.hitbox.top
            elif self.direction.y < 0:
                self.hitbox.top = sprite.hitbox.bottom

    def cooldown(self):
        """
        Verifica se o tempo de recarga (cooldown) para realizar uma ação (como um ataque) terminou.
        """
        current_time = pygame.time.get_ticks()

        if self.casting:
            if current_time - self.casting_start >= self.casting_cooldown:
                self.casting = False

    def update_particles(self):
        """
        Atualiza as partículas associadas à entidade, eliminando aquelas cujo tempo de vida expirou.
        """
        for particle in self.particles[:]:
            eliminate = particle.check_kill(self.rect.center)
            if eliminate:
                self.particles.remove(particle)
                particle.kill()

    @abstractmethod
    def animate(self):
        """
        Metodo abstrato para atualizar o sprite da entidade conforme o estado de animação atual.
        Deve ser implementado nas subclasses.
        """
        pass

    @abstractmethod
    def get_damaged(self, damage):
        """
        Metodo abstrato para aplicar dano à entidade.

        Args:
            damage (int): Quantidade de dano a ser recebida.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Metodo abstrato que define o comportamento da entidade a cada frame.
        Deve incluir movimentação, animação, lógica de colisão e ações específicas.
        """
        pass