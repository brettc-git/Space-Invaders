import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x) # Store exact position of ship horizontal float

        self.moving_left = False
        self.moving_right = False

    def update(self):
        # Update ship movement

        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)