import pygame
from settings import *

class YSortCameraGroup(pygame.sprite.Group):
    """
    Classe que gerencia o grupo de sprites para a exibição em uma câmera com ordenação em Y (Y-sorting).
    A classe herda de `pygame.sprite.Group` e permite desenhar os sprites de forma ordenada com base
    na posição vertical (eixo Y), além de permitir o deslocamento da câmera e o desenho de elementos adicionais
    como o fundo e efeitos de iluminação.

    Atributos:
        display_surface (pygame.Surface): Superfície onde os objetos são desenhados (geralmente a tela de exibição).
        half_width (int): Metade da largura da superfície de exibição.
        half_height (int): Metade da altura da superfície de exibição.
        offset (pygame.math.Vector2): Vetor usado para armazenar o deslocamento da câmera.

    Métodos:
        __init__: Inicializa o grupo de sprites e a configuração básica da câmera.
        set_floor: Define o piso do mapa a ser desenhado.
        custom_draw: Desenha todos os elementos na tela, incluindo o fundo, os sprites ordenados por Y e os efeitos de iluminação.
    """

    def __init__(self):
        """
        Inicializa o grupo de sprites e a configuração básica da câmera.

        A câmera é posicionada de forma a centralizar o personagem principal na tela.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # Obtém a superfície de exibição
        self.half_width = self.display_surface.get_size()[0] // 2  # Metade da largura da tela
        self.half_height = self.display_surface.get_size()[1] // 2  # Metade da altura da tela
        self.offset = pygame.math.Vector2()  # Inicializa o vetor de deslocamento

    def set_floor(self, floor_surf):
        """
        Define a superfície do piso a ser desenhada no fundo.

        Parâmetros:
            floor_surf (pygame.Surface): Superfície que representa o piso (fundo do mapa).
        """
        self.floor_surf = floor_surf
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))  # Define a posição do piso

    def custom_draw(self, main, second, post, post_surface):
        """
        Desenha todos os elementos na tela com base no deslocamento da câmera e na ordenação por Y.

        Este metodo desenha o fundo (piso), os sprites ordenados por Y, e os efeitos de iluminação.

        Parâmetros:
            main (pygame.sprite.Sprite): O personagem principal, usado para determinar a posição da câmera.
            second (pygame.sprite.Sprite): O segundo personagem ou elemento no jogo, utilizado para efeitos de iluminação.
            post (pygame.sprite.Group): Grupo de sprites para efeitos pós-processamento, como iluminação.
            post_surface (pygame.Surface): Superfície onde os efeitos de iluminação são desenhados.
        """
        # Obtém o deslocamento baseado na posição do personagem principal
        self.offset.x = main.rect.centerx - self.half_width
        self.offset.y = main.rect.centery - self.half_height

        # Desenha o fundo (piso)
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Desenha os sprites, ordenados por Y (baseado no centro do retângulo de cada sprite)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # Desenha os efeitos de iluminação
        for sprite in post.sprites():
            if sprite.target == 'main':
                image = sprite.image
                post_surface.blit(image,
                                  (self.half_width - image.get_width() / 2, self.half_height - image.get_height() / 2))
            elif sprite.target == 'ghost':
                offset_pos = second.rect.center - self.offset - pygame.math.Vector2(sprite.rect.width / 2,
                                                                                    sprite.rect.height / 2)
                image = sprite.image
                post_surface.blit(image, offset_pos)

        # Aplica os efeitos de iluminação na tela
        self.display_surface.blit(post_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
