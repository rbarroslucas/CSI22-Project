import pytmx
from map.obstacle import Obstacle

class TiledMap:
    """
    Classe que representa um mapa carregado a partir de um arquivo Tiled (TMX).
    Essa classe permite a manipulação e o acesso aos dados do mapa, como o tamanho e
    a criação de obstáculos com base nas camadas do mapa.

    Atributos:
        width (int): Largura do mapa em pixels, calculada com base na quantidade de tiles
                     e no tamanho de cada tile.
        height (int): Altura do mapa em pixels, calculada com base na quantidade de tiles
                      e no tamanho de cada tile.
        tmxdata (pytmx.TiledMap): Objeto contendo os dados do mapa carregados a partir do arquivo TMX.

    Métodos:
        __init__: Inicializa o mapa a partir de um arquivo TMX, calculando a largura e altura do mapa.
    """

    def __init__(self, filename):
        """
        Inicializa o mapa a partir de um arquivo TMX.

        Parâmetros:
            filename (str): Caminho para o arquivo TMX que contém os dados do mapa.

        Ação:
            Carrega os dados do mapa usando a biblioteca pytmx e calcula as dimensões
            do mapa com base no número de tiles e no tamanho de cada tile.
        """
        tm = pytmx.load_pygame(filename, pixelalpha=True)  # Carrega os dados do mapa
        self.width = tm.width * tm.tilewidth  # Calcula a largura total em pixels
        self.height = tm.height * tm.tileheight  # Calcula a altura total em pixels
        self.tmxdata = tm  # Armazena os dados carregados do mapa
