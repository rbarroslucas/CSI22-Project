import pygame, sys
from settings import *
from render.level import Level
from interfaces.pause_menu import PauseMenu
from interfaces.main_menu import MainMenu
from interfaces.game_over import GameOverMenu
from game_states import GameState

class Game:
    """
    Classe principal que gerencia o jogo, incluindo o ciclo de eventos,
    a troca de estados, a atualização da tela e a transição entre os níveis.
    """
    def __init__(self):
        """
        Inicializa o jogo, configurando a janela, os estados iniciais, o som e os níveis.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        pygame.display.set_caption('Bad Trip')
        self.clock = pygame.time.Clock()

        self.state = GameState.MAIN_MENU  # Estado inicial do jogo

        # Configuração de transições de tela (efeito de fade)
        self.fade_img = pygame.Surface((WIDTH, HEIGTH)).convert_alpha()
        self.fade_img.fill((139, 0, 0))
        self.fade = self.fade_img.get_rect()
        self.fade_alpha = 255
        self.fade_speed = 2

        # Sons de fundo e efeitos sonoros
        pygame.mixer.init()
        main_sound = pygame.mixer.Sound('./audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

        scream_sound = pygame.mixer.Sound('./audio/scream.wav')
        scream_sound.set_volume(0.5)
        scream_sound.play(loops=0)

        # Níveis do jogo
        self.levels = [None] * 4
        self.current_level = 0
        self.levels[self.current_level] = Level(f'./layouts/sala{self.current_level + 1}.tmx', False)
        self.level = self.levels[self.current_level]
        self.completed = [False for _ in self.levels]

        # Menus
        self.pauseMenu = PauseMenu()
        self.mainMenu = MainMenu()
        self.gameOverMenu = GameOverMenu()

    def run(self):
        """
        Inicia o loop principal do jogo, lidando com eventos, atualizando o estado do jogo e desenhando a tela.
        """
        while True:
            # Lida com eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Eventos agnósticos ao estado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.state in (GameState.PLAYING, GameState.PAUSED):
                        self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING

                # Eventos específicos de estado
                if self.state == GameState.MAIN_MENU:
                    action = self.mainMenu.handle_event(event)
                    if action == "new_game":
                        self.state = GameState.PLAYING
                        self.fade_alpha = 255
                        self.fade_speed = 3
                        self.set_levels()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

                elif self.state == GameState.PAUSED:
                    action = self.pauseMenu.handle_event(event)
                    if action == "continue":
                        self.state = GameState.PLAYING
                    elif action == "main_menu":
                        self.state = GameState.MAIN_MENU

                elif self.state == GameState.GAME_OVER:
                    action = self.gameOverMenu.handle_event(event)
                    if action == "retry":
                        self.state = GameState.PLAYING
                        self.set_levels()
                    elif action == "main_menu":
                        self.state = GameState.MAIN_MENU
                        self.set_levels()

            # Desenha na tela
            self.screen.fill('black')

            if self.level.is_game_over():
                self.state = GameState.GAME_OVER
            if self.state == GameState.MAIN_MENU:
                self.mainMenu.draw()
            elif self.state == GameState.GAME_OVER:
                self.gameOverMenu.draw()
            else:
                door = self.level.run(self.state)
                if door >= 0:
                    self.completed[self.current_level] = True
                    next_level = self.current_level

                    # Transição entre os níveis
                    if door == 0 and self.current_level > 0:
                        next_level -= 1
                    elif self.current_level < 3:
                        next_level += 1
                        if self.levels[next_level] is None:
                            self.levels[next_level] = Level(f'./layouts/sala{next_level + 1}.tmx', False)

                    self.transfer_func(self.current_level, next_level)
                    self.current_level = next_level
                    self.level = self.levels[self.current_level]
                    self.fade_alpha = 255
                    self.fade_speed = 3

                if self.state == GameState.PAUSED:
                    self.pauseMenu.draw()

            # Efeito de fade
            self.fade_img.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_img, self.fade)
            self.fade_alpha -= self.fade_speed
            pygame.display.update()
            self.clock.tick(FPS)

    def set_levels(self):
        """
        Configura os níveis do jogo, reiniciando o nível atual e marcando todos como não completados.
        """
        self.levels = [None] * 4
        self.current_level = 0
        self.levels[self.current_level] = Level(f'./layouts/sala{self.current_level + 1}.tmx', False)
        self.level = self.levels[self.current_level]
        self.completed = [False for _ in self.levels]

    def transfer_func(self, current, next):
        """
        Transfere informações entre os níveis, como saúde e inventário dos jogadores.
        """
        self.levels[next].player1.health = self.levels[current].player1.health
        self.levels[next].player2.health = self.levels[current].player2.health
        self.levels[next].player1.inventory = self.levels[current].player1.inventory
        self.levels[next].player2.inventory = self.levels[current].player2.inventory

        if self.levels[next].player1.check_death():
            self.levels[next].switch_player()

if __name__ == '__main__':
    game = Game()
    game.run()