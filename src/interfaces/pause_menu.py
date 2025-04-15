# interfaces/pause_menu.py
import pygame
from settings import WIDTH, HEIGTH


class PauseMenu:
    def __init__(self):
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
        """Processa eventos e retorna a ação correspondente"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None