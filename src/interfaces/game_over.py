import pygame
from settings import WIDTH, HEIGTH

class GameOverMenu:
    """
    Classe que representa o menu de "Game Over" do jogo. Exibe a tela de término de jogo com opções de
    tentar novamente ou voltar ao menu principal. A classe lida com a renderização da interface e
    a interação com o jogador através de botões.

    Atributos:
        display_surface (pygame.Surface): Superfície onde os elementos do menu serão desenhados.
        font_large (pygame.font.Font): Fonte para o título do menu.
        font_medium (pygame.font.Font): Fonte para os textos dos botões.
        overlay_color (tuple): Cor do overlay semi-transparente para o fundo.
        button_color (tuple): Cor do fundo dos botões.
        button_hover_color (tuple): Cor dos botões quando o mouse passa sobre eles.
        text_color (tuple): Cor do texto dos botões.
        buttons (list): Lista de botões com suas respectivas retângulos, textos e ações associadas.

    Métodos:
        __init__: Inicializa o menu de "Game Over", configurando as fontes, cores e botões.
        draw: Desenha a tela do menu de "Game Over", incluindo o overlay, título e botões.
        handle_event: Trata os eventos do mouse, verificando se um botão foi clicado e retornando a ação correspondente.
    """

    def __init__(self):
        """
        Inicializa a interface do menu de "Game Over" com os elementos gráficos, incluindo fontes,
        botões e cores.
        """
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

        # Cores
        self.overlay_color = (50, 0, 0, 200)  # Vermelho escuro semi-transparente
        self.button_color = (80, 0, 0, 200)
        self.button_hover_color = (120, 0, 0, 200)
        self.text_color = (255, 255, 255)

        # Botões
        button_width, button_height = 300, 70
        center_x = WIDTH // 2 - button_width // 2
        self.buttons = [
            {"rect": pygame.Rect(center_x, HEIGTH // 2, button_width, button_height), "text": "Tentar Novamente",
             "action": "retry"},
            {"rect": pygame.Rect(center_x, HEIGTH // 2 + 90, button_width, button_height), "text": "Menu Principal",
             "action": "main_menu"},
        ]

    def draw(self):
        """
        Desenha o menu de "Game Over" na tela, incluindo o título, o overlay de fundo e os botões.

        O metodo renderiza:
        - Um overlay escuro semi-transparente para o fundo.
        - O título "GAME OVER" no topo da tela.
        - Botões com texto para as ações "Tentar Novamente" e "Menu Principal".
        """
        # Overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.display_surface.blit(overlay, (0, 0))

        # Título
        title = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGTH // 4))
        self.display_surface.blit(title, title_rect)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button_surface = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            button_surface.fill(
                self.button_hover_color if button["rect"].collidepoint(mouse_pos) else self.button_color)

            self.display_surface.blit(button_surface, button["rect"].topleft)
            pygame.draw.rect(self.display_surface, (30, 0, 0, 200), button["rect"], 3, border_radius=10)

            text = self.font_medium.render(button["text"], True, self.text_color)
            self.display_surface.blit(text, text.get_rect(center=button["rect"].center))

    def handle_event(self, event):
        """
        Trata os eventos do mouse, verificando se um dos botões foi clicado.

        Args:
            event (pygame.event): O evento capturado pelo Pygame.

        Returns:
            str or None: A ação correspondente ao botão clicado ("retry", "main_menu") ou None se nenhum botão for clicado.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None