import pygame
import sys
from aliens import Aliens
from bullet import Bullet
from ship import Ship
from settings import Settings

class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Space Invaders")

        self.bg_color = self.settings.bg_color


        self.game_active = False

    def run_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()

if __name__ == "__main__":
    game = SpaceInvaders()
    game.run_game()