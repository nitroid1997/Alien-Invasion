# Alien Invasion - A pygame based space shooter game
# Copyright (C) Free-to-use  Rudra Palande
#
# Rudra Palande
# rudrap199727@gmail.com
"""This module stores the main event related functions."""

import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

# Main functionality Section.

def check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """Respond to keypress and mouse events."""
    for event in pygame.event.get():
            # for exiting the game
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

            # For ship movement to left and right.
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ai_settings,screen,ship,bullets)
            
            elif event.type == pygame.KEYUP:
                check_keyup_events(event,ship)

def update_screen(ai_settings, screen, stats,sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # redraw the screen during each pass through the loop, add bg color and draw ship and aliens on screen
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.background_image,(0,0))
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the scoreboard information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()

def check_keydown_events(event,ai_setting,screen,ship,bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, ship, bullets)

def check_keyup_events(event,ship):
    """Respond to key release."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

# Bullet Section

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responds to bullet-alien collisions and makes new fleet."""
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) # for powerfull bullet set first bool arg to false.
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # Once a fleet is destroyed, send a new fleet.
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        # Destrow existing bullet, speed up the game and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # increase level.
        sb.stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen,stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    # Get rid of bullets that have disappered the screen.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    ## print(len(bullets))  # for testing purpose.
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
    

    # Once a fleet is destroyed, send a new fleet.
    if len(aliens) == 0:
        # Destrow existing bullet and create new fleet.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if bullet limit not reached yet."""
    # create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:  # To limit the number of bullets on screen.
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

# Aliens Section

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of alien that fit in a row"""
    # Spacing between each alien is equal to one alien width.
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def get_number_row(ai_settings, ship_height, alien_height):
    """Determine the number of rows that fit on screen"""
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.x
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_row = get_number_row(ai_settings, ship.rect.height, alien.rect.height)
    
    # Create the fleet of Aliens.
    for row_number in range(number_row-ai_settings.reduce_alien_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """Check if the fleet is at an edge,and then 
    update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collision.
    if pygame.sprite.spritecollideany(ship,aliens):
        # print("Ship hit!!!") # For testing purpose
        ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets)
    
    # Look for alien hitting bottom of the screen.
    check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets)

# Statistics section.

def ship_hit(ai_settings, stats, screen,sb, ship, aliens, bullets):
    """Responds to ship being hit by aliens."""
    # Decrease ship_left (Lives)
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # Update scoreboard.
        sb.prep_ships()
        # empty alien and bullet list.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        # Reset the mouse cursor visibility.
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats,sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:                 
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats,sb,screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()