import pygame
from settings import WIDTH, HEIGTH

class PauseMenu:
    """
    Classe que representa o menu de pausa no jogo. Quando o jogo é pausado, este menu permite
    ao jogador escolher entre continuar o jogo ou voltar ao menu principal.

    Atributos:
        display_surface (pygame.Surface): A superfície onde o menu será desenhado.
        font (pygame.font.Font): Fonte usada para o título "JOGO PAUSADO".
        small_font (pygame.font.Font): Fonte usada para os textos dos botões.
        overlay_color (tuple): Cor do overlay semitransparente que cobre o fundo do menu de pausa.
        button_color (tuple): Cor dos botões no estado normal.
        button_hover_color (tuple): Cor dos botões quando o mouse passa sobre eles.
        text_color (tuple): Cor do texto exibido no menu.
        buttons (list): Lista de botões do menu, cada um com a posição, o texto e a ação associada.

    Métodos:
        __init__: Inicializa o menu de pausa com a configuração dos botões e suas ações.
        draw: Desenha o menu de pausa na tela, incluindo os botões e o título.
        handle_event: Processa os eventos de clique do mouse e retorna a ação associada ao botão clicado.
    """

    def __init__(self):
        """
        Inicializa o menu de pausa com a configuração dos botões e suas ações.
        Define as cores, fontes e a posição dos botões.
        """
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        # Cores com transparência
        self.overlay_color = (0, 0, 0, 128)
        self.button_color = (70, 70, 70, 200)
        self.button_hover_color = (100, 100, 100, 200)
        self.text_color = (255, 255, 255)

        # Botões
        button_width, button_height = 250, 60
        center_x = WIDTH // 2 - button_width // 2
        self.buttons = [
            {"rect": pygame.Rect(center_x, HEIGTH // 2 - 30, button_width, button_height), "text": "Continuar",
             "action": "continue"},
            {"rect": pygame.Rect(center_x, HEIGTH // 2 + 50, button_width, button_height), "text": "Menu Principal",
             "action": "main_menu"}
        ]

    def draw(self):
        """
        Desenha o menu de pausa na tela, incluindo o overlay transparente,
        os botões e o título "JOGO PAUSADO".
        """
        # Overlay transparente
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.display_surface.blit(overlay, (0, 0))

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            button_surface.fill(
                self.button_hover_color if button["rect"].collidepoint(mouse_pos) else self.button_color)

            self.display_surface.blit(button_surface, button["rect"].topleft)
            pygame.draw.rect(self.display_surface, (30, 30, 30, 150), button["rect"], 2, border_radius=10)

            text = self.small_font.render(button["text"], True, self.text_color)
            self.display_surface.blit(text, text.get_rect(center=button["rect"].center))

        # Título
        title = self.font.render("JOGO PAUSADO", True, self.text_color)
        self.display_surface.blit(title, title.get_rect(center=(WIDTH // 2, HEIGTH // 4)))

    def handle_event(self, event):
        """
        Processa eventos de clique do mouse e retorna a ação associada ao botão clicado.

        Parâmetros:
            event (pygame.event): O evento que foi disparado.

        Retorna:
            str: A ação do botão clicado (como "continue" ou "main_menu"), ou None se nenhum botão foi clicado.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None