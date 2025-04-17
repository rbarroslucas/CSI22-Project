import pygame
from settings import WIDTH, HEIGTH

class MainMenu:
    """
    Classe que representa o menu principal do jogo. O menu exibe uma logo e botões de navegação,
    permitindo que o jogador inicie um novo jogo ou saia.

    Atributos:
        display_surface (pygame.Surface): Superfície onde os elementos gráficos serão desenhados.
        font_large (pygame.font.Font): Fonte usada para o título e outros textos grandes.
        font_medium (pygame.font.Font): Fonte usada para os textos dos botões.
        overlay_color (tuple): Cor do overlay semi-transparente que cobre o fundo do menu.
        button_color (tuple): Cor dos botões no estado normal.
        button_hover_color (tuple): Cor dos botões quando o mouse está sobre eles.
        text_color (tuple): Cor do texto dos botões.
        image_rect (pygame.Rect): Área onde a logo do jogo será exibida.
        buttons (list): Lista de botões do menu, cada um com sua posição, texto e ação associada.
        logo_image (pygame.Surface): Imagem da logo do jogo, redimensionada para o tamanho apropriado.

    Métodos:
        __init__: Inicializa o menu, carregando a logo e configurando os botões e suas ações.
        draw: Desenha o menu na superfície de exibição, incluindo a logo e os botões.
        handle_event: Processa eventos de clique do mouse e retorna a ação correspondente ao botão pressionado.

    Ações:
        new_game (str): Ação de iniciar um novo jogo.
        quit (str): Ação de sair do jogo.
    """

    def __init__(self):
        """
        Inicializa o menu principal, configurando os botões, a logo e o overlay de fundo.
        Carrega a imagem da logo e define os parâmetros necessários para o layout dos botões.
        """
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

        # Cores
        self.overlay_color = (0, 0, 0, 200)
        self.button_color = (50, 50, 50, 200)
        self.button_hover_color = (139, 0, 0, 200)
        self.text_color = (255, 255, 255)

        # Área da imagem
        self.image_rect = pygame.Rect(WIDTH // 4, HEIGTH // 8, WIDTH // 2, HEIGTH // 3)

        # Botões
        button_width, button_height = 300, 70
        center_x = WIDTH // 2 - button_width // 2
        button_spacing = 80
        button_start_y = HEIGTH // 2 + 40

        self.buttons = [
            {"rect": pygame.Rect(center_x, button_start_y, button_width, button_height),
             "text": "Começar Jogo", "action": "new_game"},
            {"rect": pygame.Rect(center_x, button_start_y + button_spacing, button_width, button_height),
             "text": "Sair", "action": "quit"}
        ]

        self.logo_image = pygame.image.load("graphics/logo/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, self.image_rect.size)

    def draw(self):
        """
        Desenha o menu na superfície de exibição, incluindo o overlay de fundo, a logo do jogo
        e os botões de navegação. Os botões mudam de cor quando o mouse passa sobre eles.

        """
        # Fundo
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.display_surface.blit(overlay, (0, 0))

        self.display_surface.blit(self.logo_image, self.image_rect.topleft)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            button_surface.fill(
                self.button_hover_color if button["rect"].collidepoint(mouse_pos) else self.button_color)

            self.display_surface.blit(button_surface, button["rect"].topleft)
            pygame.draw.rect(self.display_surface, (30, 30, 30, 200), button["rect"], 3, border_radius=10)

            text = self.font_medium.render(button["text"], True, self.text_color)
            self.display_surface.blit(text, text.get_rect(center=button["rect"].center))

    def handle_event(self, event):
        """
        Processa eventos de clique do mouse e retorna a ação correspondente ao botão pressionado.

        Args:
            event (pygame.event.Event): O evento a ser processado.

        Retorna:
            str or None: A ação associada ao botão pressionado (ex. "new_game", "quit") ou None se nenhum botão for pressionado.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None