import pygame
import sys
from aliens import Aliens
from bullet import Bullet
from ship import Ship
from settings import Settings

class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Space Invaders")
        self.ship = Ship(self)

        self.game_active = False

    def run_game(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(60)

    def center_ship(self):
        # Center the ship on the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        self.ship.x = float(self.rect.x)

    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()

if __name__ == "__main__":
    game = SpaceInvaders()
    game.run_game()