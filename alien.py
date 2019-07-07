import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Means the class of single alien."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set the zero position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the image of alien,and set its attributes of rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Each alien originally near the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the exact position of the alien
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the image of alien at the appointed position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if the alien is at the edges of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return  True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the aliens right."""
        self.x += (self.ai_settings.alien_speed_factor*
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x


