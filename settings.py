class Settings:
    """store the all settings of alien invasion"""

    def __init__(self):
        """initialize the game's settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # The settings of the ship
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # The setting of bullet
        self.bullet_speed_factor = 6
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        # The setting of the alien
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # Accelerate the speed of the  game by some way
        self.speedup_scale = 1.4
        # aliens points improvement
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
        # 'fleet_direction' means 1 represents moving right,
        # -1 represents moving left.
        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        """initialize the settings vary with the running game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction represents that 1 means turn right and -1 means turn left
        self.fleet_direction = 1
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Improve the speed settings and aliens points."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)






