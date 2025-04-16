# interfaces/main_menu.py
import pygame
from settings import WIDTH, HEIGTH


class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

        # Cores
        self.overlay_color = (0, 0, 0, 200)
        self.button_color = (50, 50, 50, 200)
        self.button_hover_color = (80, 80, 80, 200)
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
             "text": "Novo Jogo", "action": "new_game"},
            {"rect": pygame.Rect(center_x, button_start_y + button_spacing, button_width, button_height),
             "text": "Sair", "action": "quit"}
        ]

        self.logo_image = pygame.image.load("graphics/logo/logo.png").convert_alpha()
        self.logo_image = pygame.transform.scale(self.logo_image, self.image_rect.size)

    def draw(self):
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
        """Processa eventos e retorna a ação correspondente"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None