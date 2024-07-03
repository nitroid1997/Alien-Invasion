# Alien Invasion - A pygame based space shooter game
# Copyright (C) Free-to-use  Rudra Palande
#
# Rudra Palande
# rudrap199727@gmail.com
"""In Alien Invasion, the player controls a ship that appears at
the bottom center of the screen. The player can move the ship
right and left using the arrow keys and shoot bullets using the
spacebar. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player shoots all the aliens, a new fleet
appears that moves faster than the previous fleet. If any alien hits
the player's ship or reaches the bottom of the screen, the player
loses a ship. If the player loses three ships, the game ends."""

import pygame

import game_function as gf

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """Main function that start and initialize the game"""
    # Initialize the game, settings and create a screen object

    # Initialize the background setting that pygame needs to work properly.
    pygame.init()
    ai_settings = Settings()

    # Create a display window with dimension of window as arguments and set caption to window.
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Ivasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen, stats)

    # Make a Ship.
    ship = Ship(ai_settings,screen)

    # Make an alien, for testing purpose.
    # alien = Alien(ai_settings,screen)

    # Make a group to store bullets and a group to store aliens in.
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while(True):

        # Watch for keyboard and mouse event and update bullet and ship's position.
        gf.check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens, bullets)

        # redraw the screen during each pass through the loop, add bg color and draw ship and aliens on screen
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

run_game()