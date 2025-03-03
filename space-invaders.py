import pygame
import sys
import random
from time import sleep
from pygame.sprite import Group, groupcollide

from settings import Settings
from ship import Ship
from bullet import Bullet, AlienBullet
from aliens import Aliens, PinkAlien, BlueAlien, GreenAlien, RedAlien, UFO
from barrier import Barrier
from scoreboard import Scoreboard, GameStats

class SpaceInvaders:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders")
        
        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        # Initialize ship, bullets, and aliens
        self.ship = Ship(self)
        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()
        self.barriers = []
        
        # Sound effects
        self.bullet_sound = pygame.mixer.Sound('sounds/laser.mp3')
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')
        
        # Background music
        pygame.mixer.music.load('sounds/background.mp3')
        self.music_playing = False
        self.music_speed = 1.0
        
        # UFO
        self.ufo = None
        self.last_ufo_time = 0
        
        # Game state
        self.game_active = False
        self.current_screen = "launch"  # launch, game, high_scores
        
        # Button images
        self.play_button = self._create_button("PLAY GAME", (100, 400))
        self.high_scores_button = self._create_button("HIGH SCORES", (100, 470))
        self.back_button = self._create_button("BACK", (100, 600))
        
        # For tracking time between frames
        self.last_frame_time = pygame.time.get_ticks()
        
        # Initial alien count for scaling difficulty
        self.initial_alien_count = 0
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Calculate time delta between frames
            current_time = pygame.time.get_ticks()
            time_delta = current_time - self.last_frame_time
            self.last_frame_time = current_time
            
            self._check_events()
            
            if self.current_screen == "game" and self.game_active:
                self.ship.update(time_delta)
                self._update_bullets()
                self._update_aliens(time_delta)
                self._check_bullet_collisions()
                self._check_alien_bullet_collisions()
                self._update_ufo(time_delta)
                self._fire_alien_bullets()
                
                # Update music speed based on aliens remaining
                self._update_music_speed()
            
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save high score before quitting
                if self.stats.score > 0:
                    self.stats.save_high_scores()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.current_screen == "launch":
                    self._check_play_button(mouse_pos)
                    self._check_high_scores_button(mouse_pos)
                elif self.current_screen == "high_scores":
                    self._check_back_button(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            # Save high score before quitting
            if self.stats.score > 0:
                self.stats.save_high_scores()
            sys.exit()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_rect = self.play_button[1]
        if button_rect.collidepoint(mouse_pos):
            self._start_game()
    
    def _check_high_scores_button(self, mouse_pos):
        """Show high scores screen when the player clicks High Scores."""
        button_rect = self.high_scores_button[1]
        if button_rect.collidepoint(mouse_pos):
            self.current_screen = "high_scores"
    
    def _check_back_button(self, mouse_pos):
        """Return to launch screen when the player clicks Back."""
        button_rect = self.back_button[1]
        if button_rect.collidepoint(mouse_pos):
            self.current_screen = "launch"
    
    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.game_active = True
        self.current_screen = "game"
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_ships()
        
        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        
        # Create barriers
        self._create_barriers()
        
        # Start background music
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        self.music_playing = True
        self.music_speed = 1.0
        pygame.mixer.music.set_volume(0.5)
        
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed and not self.ship.exploding:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullet_sound.play()
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        self.alien_bullets.update()
        
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
    
    def _fire_alien_bullets(self):
        """Have aliens randomly fire bullets."""
        # Randomly select aliens to fire
        for alien in self.aliens.sprites():
            # Random chance for each alien to fire
            if random.random() < self.settings.alien_firing_rate:
                new_bullet = AlienBullet(self, alien)
                self.alien_bullets.add(new_bullet)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        pink_alien = PinkAlien(self, 0, 0)
        alien_width, alien_height = pink_alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height - 200)  # 200px buffer for barriers
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Choose alien type based on row
                if row_number < 1:
                    self._create_alien(RedAlien, alien_number, row_number)
                elif row_number < 3:
                    self._create_alien(BlueAlien, alien_number, row_number)
                elif row_number < 5:
                    self._create_alien(GreenAlien, alien_number, row_number)
                else:
                    self._create_alien(PinkAlien, alien_number, row_number)
        
        # Store initial fleet size for difficulty scaling
        self.initial_alien_count = len(self.aliens)
    
    def _create_alien(self, alien_class, alien_number, row_number):
        """Create an alien and place it in the row."""
        sample_alien = alien_class(self, 0, 0)
        alien_width, alien_height = sample_alien.rect.size
        alien_width = alien_width
        alien_height = alien_height
        
        alien = alien_class(
            self,
            alien_width + 2 * alien_width * alien_number,
            alien_height + 2 * alien_height * row_number
        )
        self.aliens.add(alien)
    
    def _create_barriers(self):
        """Create the defensive barriers."""
        self.barriers = []
        
        # Create evenly spaced barriers
        screen_width = self.settings.screen_width
        barrier_count = self.settings.bunker_count
        spacing = screen_width // (barrier_count + 1)
        
        for i in range(barrier_count):
            x_position = spacing * (i + 1) - 50  # Center barrier (width is 100)
            barrier = Barrier(self, x_position)
            self.barriers.append(barrier)
    
    def _update_aliens(self, time_delta):
        """
        Check if the fleet is at an edge, then
        update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update(time_delta)
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens) and not self.ship.exploding:
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        
        self.settings.fleet_direction *= -1
    
    def _update_ufo(self, time_delta):
        """Update the UFO and randomly create new ones."""
        # Update existing UFO
        if self.ufo:
            self.ufo.update(time_delta)
            # If UFO is no longer alive, set to None
            if not self.ufo.alive():
                self.ufo = None
        
        # Randomly create new UFO
        if not self.ufo and random.random() < self.settings.ufo_appearance_rate:
            self.ufo = UFO(self)
            # Randomly choose direction (left to right or right to left)
            if random.choice([True, False]):
                self.ufo.direction = 1
                self.ufo.rect.x = -self.ufo.rect.width
            else:
                self.ufo.direction = -1
                self.ufo.rect.x = self.settings.screen_width
    
    def _update_music_speed(self):
        """Update the music speed based on number of aliens remaining."""
        if self.music_playing and self.initial_alien_count > 0:
            # Calculate percentage of aliens remaining
            alien_count = len(self.aliens)
            percentage = alien_count / self.initial_alien_count
            
            # Adjust music speed (1.0 is normal, higher is faster)
            target_speed = 1.0 + (1.0 - percentage) * 0.5  # Max speed is 1.5x
            
            # Only change if significant difference
            if abs(target_speed - self.music_speed) > 0.1:
                self.music_speed = target_speed
                pygame.mixer.music.set_volume(0.5)  # Reset volume first
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Start ship explosion animation
        self.ship.explode()
        
        # Pause the game briefly
        sleep(0.5)
        
        # Decrement ships_left
        self.stats.ships_left = self.ship.lives
        self.sb.prep_ships()
        
        if self.stats.ships_left > 0:
            # Center the ship
            self.ship.center_ship()
            
            # Clear alien bullets
            self.alien_bullets.empty()
        else:
            self.game_active = False
            self.current_screen = "launch"
            pygame.mouse.set_visible(True)
            
            # Stop music
            if self.music_playing:
                pygame.mixer.music.stop()
                self.music_playing = False
            
            # Save high score
            self.stats.save_high_scores()
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
    
    def _check_bullet_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for bullets that hit aliens
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)
        
        # Process alien hits
        if collisions:
            for bullet, aliens_hit in collisions.items():
                for alien in aliens_hit:
                    # Start alien explosion animation
                    alien.hit()
                    self.explosion_sound.play()
                    
                    # Add points for each alien hit
                    self.stats.score += alien.point_value
            
            self.sb.prep_score()
            self.sb.check_high_score()
        
        # Check for bullet-UFO collisions
        if self.ufo and pygame.sprite.spritecollideany(self.ufo, self.bullets):
            # Remove the bullet
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, self.ufo):
                    bullet.kill()
            
            # Start UFO hit sequence
            self.ufo.hit()
            self.explosion_sound.play()
            
            # Add points
            self.stats.score += self.ufo.point_value
            self.sb.prep_score()
            self.sb.check_high_score()
        
        # Check for bullet-barrier collisions
        for barrier in self.barriers:
            pygame.sprite.groupcollide(
                self.bullets, barrier.pieces, True, False)
            for piece, bullets_hit in pygame.sprite.groupcollide(
                    barrier.pieces, self.bullets, False, True).items():
                piece.hit()
        
        # Check if all aliens have been destroyed
        if not self.aliens:
            # Destroy all bullets and create new fleet
            self.bullets.empty()
            self.alien_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed(len(self.aliens), self.initial_alien_count)
    
    def _check_alien_bullet_collisions(self):
        """Check for alien bullets colliding with ship or barriers."""
        # Check for alien bullets hitting the ship
        if not self.ship.exploding and pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            # Remove the bullet
            for bullet in self.alien_bullets:
                if pygame.sprite.collide_rect(bullet, self.ship):
                    bullet.kill()
            
            # Handle ship hit
            self._ship_hit()
        
        # Check for alien bullets hitting barriers
        for barrier in self.barriers:
            for piece, bullets_hit in pygame.sprite.groupcollide(
                    barrier.pieces, self.alien_bullets, False, True).items():
                piece.hit()
        
        # Check for bullet-bullet collisions (cancel each other out)
        pygame.sprite.groupcollide(self.bullets, self.alien_bullets, True, True)
    
    def _create_button(self, text, position):
        """Create a button with text and position."""
        button_color = (0, 255, 0)
        text_color = (255, 255, 255)
        font = pygame.font.SysFont('Arial', 48)
        
        # Render the text
        text_image = font.render(text, True, text_color)
        text_rect = text_image.get_rect()
        text_rect.topleft = position
        
        # Create button rectangle
        button_rect = text_rect.inflate(40, 20)
        
        return ((text_image, text_rect), button_rect)
    
    def _draw_launch_screen(self):
        """Draw the launch screen."""
        # Fill background
        self.screen.fill(self.settings.bg_color)
        
        # Draw game title
        title_font = pygame.font.SysFont('Arial', 80)
        title_text = title_font.render("SPACE INVADERS", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.screen.get_rect().centerx, y=100)
        self.screen.blit(title_text, title_rect)
        
        # Draw alien values
        value_font = pygame.font.SysFont('Arial', 36)
        
        # Sample aliens at different positions
        sample_aliens = [
            (RedAlien(self, 0, 0), "= 40 POINTS", (255, 0, 0)),
            (BlueAlien(self, 0, 0), "= 20 POINTS", (0, 0, 255)),
            (GreenAlien(self, 0, 0), "= 10 POINTS", (0, 255, 0)),
            (PinkAlien(self, 0, 0), "= 30 POINTS", (255, 0, 255)),
            (UFO(self), "= ???", (255, 255, 255))
        ]
        
        # Display each alien and its value
        for i, (alien, value_str, color) in enumerate(sample_aliens):
            # Position alien
            x_pos = self.screen.get_rect().centerx - 100
            y_pos = 200 + i * 50
            
            # Render alien
            self.screen.blit(alien.image, (x_pos, y_pos))
            
            # Render value text
            value_text = value_font.render(value_str, True, color)
            self.screen.blit(value_text, (x_pos + 60, y_pos))
        
        # Draw buttons
        (button_text, button_text_rect), button_rect = self.play_button
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect, 3)
        self.screen.blit(button_text, button_text_rect)
        
        (button_text, button_text_rect), button_rect = self.high_scores_button
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect, 3)
        self.screen.blit(button_text, button_text_rect)
    
    def _draw_high_scores_screen(self):
        """Draw the high scores screen."""
        # Fill background
        self.screen.fill(self.settings.bg_color)
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 64)
        title_text = title_font.render("HIGH SCORES", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.screen.get_rect().centerx, y=50)
        self.screen.blit(title_text, title_rect)
        
        # Draw scores
        score_font = pygame.font.SysFont('Arial', 36)
        
        for i, score_data in enumerate(self.stats.high_scores):
            name = score_data["name"]
            score = score_data["score"]
            
            # Format score text
            text = f"{i+1}. {name}: {score}"
            score_text = score_font.render(text, True, (255, 255, 255))
            
            # Position text
            x_pos = self.screen.get_rect().centerx - score_text.get_width() // 2
            y_pos = 150 + i * 40
            
            # Draw text
            self.screen.blit(score_text, (x_pos, y_pos))
        
        # Draw back button
        (button_text, button_text_rect), button_rect = self.back_button
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect, 3)
        self.screen.blit(button_text, button_text_rect)
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        if self.current_screen == "launch":
            self._draw_launch_screen()
        elif self.current_screen == "high_scores":
            self._draw_high_scores_screen()
        elif self.current_screen == "game":
            # Background
            self.screen.fill(self.settings.bg_color)
            
            # Draw ship
            self.ship.blitme()
            
            # Draw bullets
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()
            
            # Draw aliens
            self.aliens.draw(self.screen)
            
            # Draw UFO if active
            if self.ufo:
                self.screen.blit(self.ufo.image, self.ufo.rect)
            
            # Draw barriers
            for barrier in self.barriers:
                barrier.draw()
            
            # Draw the score information
            self.sb.show_score()
        
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    game = SpaceInvaders()
    game.run_game()
