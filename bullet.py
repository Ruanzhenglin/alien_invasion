import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """The class of the management of the bullet to the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Building the object of bullet at the position of the ship"""
        super().__init__()
        self.screen = screen

        # Building the rectangle which represents the shape of the bullet,
        # and setting the correct position at the location of (0, 0).
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # The decimals that represent the position of the bullet
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet upward"""
        # Updating the value of decimals of rect of the bullet's position
        self.y -= self.speed_factor
        # Updating the rect that represents the position of the bullet
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

