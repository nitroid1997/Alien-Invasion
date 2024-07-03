# Alien Invasion - A pygame based space shooter game
# Copyright (C) Free-to-use  Rudra Palande
#
#Rudra Palande
#rudrap199727@gmail.com
"""This module contains all the required game settings."""

import pygame

class Settings():
    """A class to store all settings for alien Invasion"""

    def __init__(self) -> None:
        """Initialize the gams's settings."""
        # Screen settings and background color.
        self.screen_width = 1200
        self.screen_height = 800
        # Fullscreen setting.
        # self.screen_width = 1920
        # self.screen_height = 1080
        self.bg_color = (10,0,10)
        self.bg_scoreboard_color = (255,0,0)
        self.background_image = pygame.image.load("Resources/Images/Extras/background_2.jpg") 

        # Ship settings.
        self.ship_speed_factor = 1.5
        self.ship_limit = 2

        # Bullet settings.
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 0, 255, 255
        self.bullets_allowed = 4

        # Difficult setting to reduce alien rows.
        self.reduce_alien_rows = 3

        # Alien settings.
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 8
        # fleet direction of 1 represent right; -1 represent left.
        self.fleet_direction = 1

        # How quickely the game speeds up.
        self.speedup_scale = 1.1

        # How quickely the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # Asset manager.
        self.ship_selector = 1  # Used to change ship model.

        # Scoring.
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

         
