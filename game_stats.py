# Alien Invasion - A pygame based space shooter game
# Copyright (C) Free-to-use  Rudra Palande
#
#Rudra Palande
#rudrap199727@gmail.com
"""This module contains all the required game scoring and stats details."""

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings) -> None:
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        # High score should never be reset.
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

