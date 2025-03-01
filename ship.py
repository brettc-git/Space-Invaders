import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self):

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()


        self.moving_left = False
        self.moving_right = False