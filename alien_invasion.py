import sys
from time import sleep

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from bullet import Bullet
from alien import Alien

from ship import Ship
import game_functions as gf


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.ai_settings = Settings()



        self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self.ai_settings)
        self.sb = Scoreboard(self.ai_settings, self.screen, self.stats)

        self.ship = Ship(self.ai_settings, self.screen)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        print(self.aliens)

        gf.create_fleet(self.ai_settings, self.screen, self.ship, self.aliens)

        # Make the Play button.
        self.play_button = Button(self.ai_settings, self.screen, "Play")


    def run_game(self):
        # start the main loop of the game
        while True:
            # supervise the event of mouse and keyboard
            gf.check_events(self.ai_settings, self.screen, self.stats, self.sb, self.play_button, self.ship,
                            self.aliens, self.bullets)

            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets)
                gf.update_aliens(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets)

            gf.update_screen(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.bullets,
                            self.play_button)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()