from items.potion import Potion

class DurationPotion(Potion):
    """
    Classe que representa uma poção com um efeito de buff temporário.
    Ela herda da classe `Potion` e adiciona uma duração para o buff aplicado.

    Atributos:
        name (str): O nome da poção.
        buff (str): O efeito de buff fornecido pela poção.
        image (pygame.Surface): A imagem que representa a poção.
        buff_duration (int): A duração do efeito de buff, em segundos.

    Métodos:
        __init__: Inicializa a poção com um nome, um buff, uma imagem e a duração do buff.
    """

    def __init__(self, name, buff, buff_duration, image):
        """
        Inicializa a poção de duração com os atributos necessários,
        incluindo o nome, buff, imagem e a duração do buff.

        Parâmetros:
            name (str): O nome da poção.
            buff (str): O efeito de buff fornecido pela poção.
            buff_duration (int): A duração do efeito de buff, em segundos.
            image (pygame.Surface): A imagem que representa a poção.
        """
        super().__init__(name, buff, image)
        self.buff_duration = buff_duration