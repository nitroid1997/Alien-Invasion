# Alien Invasion - A pygame based space shooter game
# Copyright (C) Free-to-use  Rudra Palande
#
#Rudra Palande
#rudrap199727@gmail.com
"""This modules contains all the details and information 
related to player ship."""

import pygame

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen) -> None:
        """Initialize the ship and set it's starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Load the ship image and get it's rect.
        if ai_settings.ship_selector == 1:
            self.image = pygame.image.load('Resources/Images/Ships/rocket.png')
        elif ai_settings.ship_selector == 2:
            self.image = pygame.image.load('Resources/Images/Extras/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Move the ship to right and left, and keep it in boundaries of screen.
        # Update the ship's center value not rectangle.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            ## self.rect.centerx += 1  # Old way of movement of updating ship's rect value.
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            ## self.rect.centerx -= 1  # Old way of movement of updating ship's rect value.
            self.center -= self.ai_settings.ship_speed_factor
        
        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship in it's current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on screen"""
        self.center = self.screen_rect.centerx