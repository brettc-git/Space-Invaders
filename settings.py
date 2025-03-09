# COLORS
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = BLACK
        
        # Ship settings
        self.ship_limit = 3  # Amount of lives player can have
        self.ship_speed = 3.5
        
        # Bullet settings
        self.bullet_speed = 7.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = WHITE
        self.bullets_allowed = 3
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 represents right; -1 represents left
        
        # Alien bullet settings
        self.alien_bullet_speed = 3.0
        self.alien_bullet_width = 3
        self.alien_bullet_height = 15
        self.alien_bullet_color = WHITE
        self.alien_firing_rate = 0.0005  # Probability of an alien firing per frame
        
        # UFO settings
        self.ufo_speed = 2.0
        self.ufo_appearance_rate = 0.001  # Probability of UFO appearing per frame
        
        # Bunker settings
        self.bunker_count = 4
        
        # Game speed settings
        self.speedup_scale = 1.1  # How much the game speeds up as aliens are destroyed
        self.score_scale = 1.5
        
        # How quickly the alien point values increase
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0
        self.fleet_direction = 1
        self.alien_points = 50
        
    def increase_speed(self, alien_count, initial_alien_count):
        # Calculate the percentage of aliens left
        percentage_remaining = alien_count / initial_alien_count
        
        # Adjust speed inversely to the percentage of aliens remaining
        # The fewer aliens, the faster they move
        if percentage_remaining < 0.75:
            self.alien_speed = 1.0 * (1.0 + (0.75 - percentage_remaining) * 3)
