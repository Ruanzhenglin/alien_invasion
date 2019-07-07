class GameStats():
    """Tracking the statistical information of the game."""

    def __init__(self, ai_settings):
        """Initialising the statistical information."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Let the game be in inactive
        self.game_active = False
        # shouldn't reset the score at any situation
        self.high_score = 0

    def reset_stats(self):
        """Initialising the statistical information of the period of running the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

        # Be in active state when the game starts
        self.game_active = True


