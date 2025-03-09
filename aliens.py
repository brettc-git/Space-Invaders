import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """base class for all alien types"""
    def __init__(self, game, x, y):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        
        # Animation states
        self.frames = []
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 1000  # milliseconds between frames
        
        # Movement
        self.x = float(x)
        self.y = float(y)
        self.speed_factor = 1.0
        
        # State
        self.dying = False
        self.explosion_frames = []
        self.explosion_frame = 0
        self.explosion_time = 0
        self.explosion_speed = 100  # milliseconds between explosion frames
        
    def update(self, time_delta):
        # Handle animation
        self.frame_time += time_delta
        if self.frame_time > self.animation_speed:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        
        # Handle explosion animation if dying
        if self.dying:
            self.explosion_time += time_delta
            if self.explosion_time > self.explosion_speed:
                self.explosion_time = 0
                if self.explosion_frame < len(self.explosion_frames) - 1:
                    self.explosion_frame += 1
                    self.image = self.explosion_frames[self.explosion_frame]
                else:
                    self.kill()  # Remove sprite when explosion animation completes
        
        # Update position based on current speed
        self.x += self.settings.alien_speed * self.speed_factor * self.settings.fleet_direction
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False
    
    def hit(self):
        """start explosion animation when hit by bullet"""
        if not self.dying:
            self.dying = True
            self.explosion_frame = 0
            self.explosion_time = 0
            self.image = self.explosion_frames[0]
            # Play explosion sound
            pygame.mixer.Sound('sounds/alien_explosion.mp3').play()

class PinkAlien(Aliens):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Load the two animation frames
        self.frames = [
            pygame.image.load('images/pink_alien_1.png'),
            pygame.image.load('images/pink_alien_2.png')
        ]
        # Load explosion animation frames
        self.explosion_frames = [
            pygame.image.load('images/pink_alien_explosion_1.png'),
            pygame.image.load('images/pink_alien_explosion_2.png'),
            pygame.image.load('images/pink_alien_explosion_3.png')
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.point_value = 30

class BlueAlien(Aliens):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Load the two animation frames
        self.frames = [
            pygame.image.load('images/blue_alien_1.png'),
            pygame.image.load('images/blue_alien_2.png')
        ]
        # Load explosion animation frames
        self.explosion_frames = [
            pygame.image.load('images/blue_alien_explosion_1.png'),
            pygame.image.load('images/blue_alien_explosion_2.png'),
            pygame.image.load('images/blue_alien_explosion_3.png')
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.point_value = 20

class GreenAlien(Aliens):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Load the two animation frames
        self.frames = [
            pygame.image.load('images/green_alien_1.png'),
            pygame.image.load('images/green_alien_2.png')
        ]
        # Load explosion animation frames
        self.explosion_frames = [
            pygame.image.load('images/green_alien_explosion_1.png'),
            pygame.image.load('images/green_alien_explosion_2.png'),
            pygame.image.load('images/green_alien_explosion_3.png')
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.point_value = 10

class RedAlien(Aliens):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # Load the two animation frames
        self.frames = [
            pygame.image.load('images/red_alien_1.png'),
            pygame.image.load('images/red_alien_2.png')
        ]
        # Load explosion animation frames
        self.explosion_frames = [
            pygame.image.load('images/red_alien_explosion_1.png'),
            pygame.image.load('images/red_alien_explosion_2.png'),
            pygame.image.load('images/red_alien_explosion_3.png')
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.point_value = 40

class UFO(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        
        # Load the UFO image
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        
        # Set starting position (top of screen, off to the left)
        self.rect.y = 50
        self.rect.x = -self.rect.width
        
        # Store decimal position
        self.x = float(self.rect.x)
        
        # Sound
        self.sound = pygame.mixer.Sound('sounds/ufo_sound.mp3')
        self.sound_playing = False
        
        # Points (random value when destroyed)
        self.possible_values = [50, 100, 150, 300]
        self.point_value = 0
        self.showing_value = False
        self.value_display_time = 0
        self.value_max_time = 1000  # milliseconds to show value
        
        # Direction (1 = right, -1 = left)
        self.direction = 1
        
    def update(self, time_delta):
        # Move the UFO
        self.x += self.settings.ufo_speed * self.direction
        self.rect.x = self.x
        
        # Play sound if not already playing
        if not self.sound_playing:
            self.sound.play(-1)  # Loop indefinitely
            self.sound_playing = True
            
        # Check if UFO has moved off screen
        screen_rect = self.screen.get_rect()
        if (self.direction > 0 and self.rect.left > screen_rect.right) or \
           (self.direction < 0 and self.rect.right < 0):
            self.kill()
            if self.sound_playing:
                self.sound.stop()
                self.sound_playing = False
        
        # Handle value display if hit
        if self.showing_value:
            self.value_display_time += time_delta
            if self.value_display_time >= self.value_max_time:
                self.kill()
                if self.sound_playing:
                    self.sound.stop()
                    self.sound_playing = False
    
    def hit(self):
        if not self.showing_value:
            import random
            self.showing_value = True
            self.value_display_time = 0
            self.point_value = random.choice(self.possible_values)
            
            # Create a font to display the value
            font = pygame.font.SysFont('Arial', 28)
            self.image = font.render(str(self.point_value), True, (255, 255, 255))
            
            # Stop the UFO sound and play explosion
            if self.sound_playing:
                self.sound.stop()
                self.sound_playing = False
            pygame.mixer.Sound('sounds/ufo_explosion.mp3').play()
