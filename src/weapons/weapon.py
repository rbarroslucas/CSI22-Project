import pygame

class Weapon:
    """
    Classe que representa uma arma no jogo, com atributos de nome, dano e tempo de recarga,
    além de buffs temporários para dano e recarga.

    Atributos:
        name (str): Nome da arma.
        damage (int): Dano base da arma.
        cooldown (int): Tempo de recarga da arma (em milissegundos).
        damage_buff (int): Valor do aumento de dano aplicado temporariamente.
        damage_buff_duration (int): Duração do buff de dano.
        cooldown_buff (int): Valor da redução de recarga aplicado temporariamente.
        cooldown_buff_duration (int): Duração do buff de recarga.
        weapon_image (pygame.Surface): Imagem da arma.
    """

    def __init__(self, name, damage, cooldown):
        """
        Inicializa uma nova instância de arma com atributos de dano, recarga e buffs temporários.

        Parâmetros:
            name (str): Nome da arma.
            damage (int): Dano base da arma.
            cooldown (int): Tempo de recarga da arma.
        """
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.damage_buff = 0
        self.damage_buff_duration = 0
        self.cooldown_buff = 0
        self.cooldown_buff_duration = 0

        # Carrega a imagem da arma
        self.weapon_image = pygame.image.load("graphics/arma/arma.png").convert_alpha()
