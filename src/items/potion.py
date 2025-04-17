import pygame

class Potion:
    """
    Classe que representa uma poção no jogo. Cada poção possui um nome, um efeito de buff
    e uma imagem associada.

    Atributos:
        name (str): O nome da poção.
        buff (str): O efeito de buff fornecido pela poção.
        image (pygame.Surface): A imagem que representa a poção.

    Métodos:
        __init__: Inicializa a poção com um nome, buff e imagem.
    """

    def __init__(self, name, buff, image):
        """
        Inicializa a poção com o nome, buff e imagem fornecidos.

        Parâmetros:
            name (str): O nome da poção.
            buff (str): O efeito de buff fornecido pela poção.
            image (pygame.Surface): A imagem que representa a poção.
        """
        self.name = name
        self.buff = buff
        self.image = image