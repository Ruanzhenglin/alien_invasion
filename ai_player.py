from random import random 
import pygame
from alien_invasion import AlienInvasion 

import game_functions as gf

class AIPlayer:

    def __init__(self, ai_game):                                        # 1
        """Automatic player for Alien Invasion."""

        # Need a reference to the game object.
        self.ai_game = ai_game                                          # 2

    def run_game(self):                                                 # 3
        """Replaces the original run_game(), so we can interject our own
        controls.
        """

        # Start out in an active state.
        self.ai_game.stats.game_active = True                           # 4
        pygame.mouse.set_visible(False)

        # Speed up the game for development work.
        self.modify_speed(5)

        # Get the full fleet size.
        self.fleet_size = len(self.ai_game.aliens)

        # Start the main loop for the game.
        while True:                                                     # 5
            # Still call ai_game._check_events(), so we can use keyboard to
            #   quit.
            gf.check_events(ai_game.ai_settings, ai_game.screen, ai_game.stats, ai_game.sb, ai_game.play_button, ai_game.ship,
                            ai_game.aliens, ai_game.bullets)  
            self.implement_strategy()

            if self.ai_game.stats.game_active:
                self.ai_game.ship.update()
                gf.update_bullets(ai_game.ai_settings, ai_game.screen, ai_game.stats, ai_game.sb, ai_game.ship, ai_game.aliens, ai_game.bullets)
                gf.update_aliens(ai_game.ai_settings, ai_game.screen, ai_game.stats, ai_game.sb, ai_game.ship, ai_game.aliens, ai_game.bullets)               
                gf.fire_bullet(ai_game.ai_settings, ai_game.screen, ai_game.ship, ai_game.bullets)
            

            gf.update_screen(ai_game.ai_settings, ai_game.screen, ai_game.stats, ai_game.sb, ai_game.ship, ai_game.aliens, ai_game.bullets,ai_game.play_button)


    def implement_strategy(self):
        """Implement an automated strategy for playing the game."""

        # Sweep right and left until half the fleet is destroyed, then stop.
        if len(self.ai_game.aliens) >= 0.5 * self.fleet_size:
            self.sweep_right_left() 

        else:
            self.ai_game.ship.moving_right = False
            self.ai_game.ship.moving_left = False     

        # Get specific alien to chase.
        if self.ai_game.aliens.sprites():
            target_alien = self.get_target_alien()                         # 1

            # Move toward target alien.
            ship = self.ai_game.ship
            if ship.rect.x < target_alien.rect.x:                           # 2
                ship.moving_right = True
                ship.moving_left = False
            elif ship.rect.x > target_alien.rect.x:
                ship.moving_right = False
                ship.moving_left = True

        # Fire a bullet at the given frequency, whenever possible.
        firing_frequency = 1.0                                          # 2
        if random() < firing_frequency:
            gf.fire_bullet(ai_game.ai_settings, ai_game.screen, ai_game.ship, ai_game.bullets)


    def get_target_alien(self):
        """Get a specific alien to target."""
        # Find the right-most alien in the bottom row.
        #   Pick the first alien in the group. Then compare all others, 
        #   and return the alien with the greatest x and y rect attributes.
        if len(self.ai_game.aliens.sprites()) != 0:

            target_alien = self.ai_game.aliens.sprites()[0]             # 3 something is wrong 
            for alien in self.ai_game.aliens.sprites():
                if alien.rect.y > target_alien.rect.y:                      # 4
                    # This alien is farther down than target_alien.
                    target_alien = alien
                elif alien.rect.y < target_alien.rect.y:                    # 5
                    # This alien is above target_alien.
                    continue
                elif alien.rect.x > target_alien.rect.x:                    # 6
                    # This alien is in the same row, but farther right.
                    target_alien = alien
            return target_alien


    def sweep_right_left(self):
        """Sweep the ship right and left continuously."""
        ship = self.ai_game.ship
        screen_rect = self.ai_game.screen.get_rect()

        if not ship.moving_right and not ship.moving_left:
            # Ship hasn't started moving yet; move to the right.
            ship.moving_right = True
        elif (ship.moving_right
                    and ship.rect.right > screen_rect.right - 10):
            # Ship about to hit right edge; move left.
            ship.moving_right = False
            ship.moving_left = True
        elif ship.moving_left and ship.rect.left < 10:
            ship.moving_left = False
            ship.moving_right = True

    def modify_speed(self, speed_factor):                              # 2
        self.ai_game.ai_settings.ship_speed_factor += speed_factor
        self.ai_game.ai_settings.bullet_speed_factor += speed_factor
        self.ai_game.ai_settings.alien_speed_factor += speed_factor   

     
if __name__ == '__main__':
    ai_game = AlienInvasion()

    ai_player = AIPlayer(ai_game)
    ai_player.run_game()