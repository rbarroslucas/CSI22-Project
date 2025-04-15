# interfaces/game_over_menu.py
import pygame
from settings import WIDTH, HEIGTH


class GameOverMenu:
    def __init__(self):
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
            {"rect": pygame.Rect(center_x, HEIGTH // 2 + 180, button_width, button_height), "text": "Sair",
             "action": "quit"}
        ]

    def draw(self):
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None