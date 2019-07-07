import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        """initialize the ship and set the initial location"""
        self.screen = screen
        self.ai_settings = ai_settings

        # load the image of ship and get its exterior rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Put the every new ship on the centre at bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store the decimals in the attributes of the ship of center
        self.center = float(self.rect.centerx)

        # Moving signal
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Adjust the position if the ship according to
        the signal of the ship's position.
        """
        # Updating the value of the center of the ship, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Updating the object of rect according to the self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at the appointed location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Let the ship in the middle of the bottom of screen"""
        self.center = self.screen_rect.centerx


