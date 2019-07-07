import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button

from ship import Ship
import game_functions as gf


def run_game():
    # initialize the game and build a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create a example for restoring the statistical information of game.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Set the background color.
    bg_color = (230, 230, 230)

    # Create the button of Play
    play_button = Button(ai_settings, screen, "Play")

    # Create a ship a group of bullet and a group of alien
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create a group of alien
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # start the main loop of the game
    while True:

        # supervise the event of mouse and keyboard
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()


