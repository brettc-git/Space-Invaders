import pygame.font
import json
import os

class Scoreboard:
    """A class to report scoring information."""
    
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Arial', 48)
        
        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        # Load high score from file if it exists
        self._load_high_score()
        
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HIGH: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = []
        for ship_number in range(self.stats.ships_left):
            ship = pygame.image.load('images/ship.png')
            ship_rect = ship.get_rect()
            ship_rect.x = 10 + ship_number * (ship_rect.width + 10)
            ship_rect.y = 10
            self.ships.append((ship, ship_rect))
    
    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        # Draw ships
        for ship, ship_rect in self.ships:
            self.screen.blit(ship, ship_rect)
    
    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self._save_high_score()
    
    def _load_high_score(self):
        """Load high score from a file."""
        try:
            with open('high_score.json', 'r') as f:
                self.stats.high_score = json.load(f)
        except FileNotFoundError:
            self.stats.high_score = 0
    
    def _save_high_score(self):
        """Save high score to a file."""
        with open('high_score.json', 'w') as f:
            json.dump(self.stats.high_score, f)

class GameStats:
    """Track statistics for Space Invaders."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Start game in an inactive state
        self.game_active = False
        
        # High score should never be reset
        self.high_score = 0
        
        # Load high scores list for high score screen
        self.high_scores = []
        self._load_high_scores()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
    
    def _load_high_scores(self):
        """Load high scores list from a file."""
        try:
            with open('high_scores.json', 'r') as f:
                self.high_scores = json.load(f)
        except FileNotFoundError:
            self.high_scores = []
    
    def save_high_scores(self, name="ANON"):
        """Save current score to high scores list."""
        self.high_scores.append({"name": name, "score": self.score})
        # Sort by score (highest first)
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)
        # Keep only top 10
        self.high_scores = self.high_scores[:10]
        # Save to file
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_scores, f)
