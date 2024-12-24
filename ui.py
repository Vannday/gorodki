#ui.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font
        self.action = action
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

class Label:
    def __init__(self, x, y, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.text_surface = font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(topleft=(x, y))

    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)
        self.text_rect = self.text_surface.get_rect(topleft=self.text_rect.topleft)

    def draw(self, surface):
        surface.blit(self.text_surface, self.text_rect)