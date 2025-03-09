import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store decimal positions for the ship's horizontal and vertical positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        # Ship status
        self.lives = self.settings.ship_limit
        self.exploding = False
        self.explosion_frame = 0
        self.explosion_frames = []
        self.explosion_time = 0
        self.explosion_speed = 100  # milliseconds between explosion frames
        
        # Load explosion animation frames
        for i in range(1, 9):  # 8 frames of explosion
            self.explosion_frames.append(
                pygame.image.load(f'images/ship_explosion_{i}.png')
            )
    
    def update(self, time_delta=None):
        """Update the ship's position based on movement flags."""
        # Handle explosion animation if exploding
        if self.exploding and time_delta:
            self.explosion_time += time_delta
            if self.explosion_time > self.explosion_speed:
                self.explosion_time = 0
                if self.explosion_frame < len(self.explosion_frames) - 1:
                    self.explosion_frame += 1
                    self.image = self.explosion_frames[self.explosion_frame]
                else:
                    self.exploding = False
                    self.image = pygame.image.load('images/ship.png')
                    self.center_ship()
        
        # Movement updates (only if not exploding)
        if not self.exploding:
            # Update horizontal position
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed
                
            # Update vertical position (with boundaries to keep ship in lower portion)
            if self.moving_up and self.rect.top > self.screen_rect.height * 0.7:  # Upper boundary
                self.y -= self.settings.ship_speed
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ship_speed
            
            # Update rect object from position variables
            self.rect.x = self.x
            self.rect.y = self.y
    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Reset movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        
    def explode(self):
        if not self.exploding:
            self.exploding = True
            self.explosion_frame = 0
            self.explosion_time = 0
            self.image = self.explosion_frames[0]
            # Play explosion sound
            pygame.mixer.Sound('sounds/ship_explosion.mp3').play()
            
            # Decrement lives
            self.lives -= 1
