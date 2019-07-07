import sys
from time import sleep


import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Response to pressing the key"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """If not reach the upper limit, then fire a bullet."""
    # Build a bullet, and add it to the group of the bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Response to the releasing the key"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Response to mouse and keyboard"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Start game when the player press the button of Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the settings of the game.
        ai_settings.initialize_dynamic_settings()
        # Conceal the cursor
        pygame.mouse.set_visible(False)
        # Reset the statistical information of game
        stats.reset_stats()
        stats.game_active = True

        # Reset the image of scoreboard.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Clean the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new group of the aliens, and let ship be middle
        #  of the screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """Update the images on the screen,and jump to a new screen"""
    # Re_plot the picture on the screen each time loop
    screen.fill(ai_settings.bg_color)
    # Redraw the all bullets in the back of ships and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Show the score
    sb.show_score()

    # Draw the Play button if the game is in inactive
    if not stats.game_active:
        play_button.draw_button()

    # Let the nearest updating screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update the position of the bullet, and delete the vanished bullets."""

    # Update the position of the bullets
    bullets.update()

    # delete the vanished bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to the collisions of aliens and the bullets"""
    """Delete the colliding bullets and the aliens """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Up grading if all aliens is wiped out
        bullets.empty()
        ai_settings.increase_speed()

        # Improve the level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Calculate the number of the aliens on each line"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Calculate the number of rows that the screen could accommodate."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and add it to the current line"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create the a group of aliens"""
    # Create an alien and calculate the number of the aliens that each
    # line could accommodate.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the groups of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    """Take the corresponding actions when the alien is at the edges of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Move the whole aliens down and change their directions"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets):
    """Check whether aliens reach the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Solve this situation just like the ship collided by aliens
            ship_hit(ai_settings, screen, stats, sb, ship, aliens,
                     bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check whether the aliens is at the edges of the screen and update
    all the position of the aliens among the groups of aliens.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detect the collisions of aliens and the ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings,  screen, stats, sb, ship, aliens, bullets)

    # Detect whether the aliens is at the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responding to the ships collided by the aliens"""
    if stats.ships_left > 0:
        # ships_left minus 1
        stats.ships_left -= 1

        # Updating the scoreboard
        sb.prep_ships()

        # Clean the list of aliens and the list bullets clear by respect.
        aliens.empty()
        bullets.empty()

        # Create a group of new aliens, and put the ships at the bottom of the screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """Check whether the new score generate."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


