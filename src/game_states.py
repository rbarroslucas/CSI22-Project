# game_states.py
from enum import Enum, auto

class GameState(Enum):
    """
    Enumeração que representa os diferentes estados do jogo.

    Cada estado corresponde a uma fase ou situação em que o jogo pode se encontrar.
    Isso permite que o fluxo do jogo seja controlado e alternado de forma organizada.

    Estados possíveis:
        MAIN_MENU (0): Menu principal do jogo.
        PLAYING (1): O jogo está em andamento.
        PAUSED (2): O jogo está pausado.
        INVENTORY (3): O jogador está visualizando o inventário.
        GAME_OVER (4): O jogo terminou, exibindo a tela de fim de jogo.
    """
    MAIN_MENU = auto()    # Estado quando o jogador está no menu principal
    PLAYING = auto()      # Estado enquanto o jogo está sendo jogado
    PAUSED = auto()       # Estado quando o jogo está pausado
    INVENTORY = auto()    # Estado quando o jogador está visualizando o inventário
    GAME_OVER = auto()    # Estado quando o jogo termina
