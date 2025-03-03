import pygame
import random
from pygame.sprite import Sprite, Group
from PIL import Image, ImageDraw

class BarrierPiece(Sprite):
    """A single piece of the barrier that can be damaged."""
    def __init__(self, barrier, x, y, width, height, color):
        super().__init__()
        self.screen = barrier.screen
        self.color = color
        
        # Create the piece's rect and set its position
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.x = x
        self.rect.y = y
        
        # Create a surface for the piece
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        # Damage level (0-100%)
        self.damage = 0
    
    def hit(self):
        """Damage the barrier piece when hit by a bullet."""
        # Increase damage
        self.damage += 25
        
        # If damage is too high, destroy the piece
        if self.damage >= 100:
            self.kill()
            return
        
        # Otherwise, create a transparent effect by removing random pixels
        # Convert pygame surface to PIL Image
        pil_image = Image.frombytes('RGBA', self.image.get_size(), 
                                    pygame.image.tostring(self.image, 'RGBA'))
        
        # Create a drawing object
        draw = ImageDraw.Draw(pil_image)
        
        # Determine how many pixels to make transparent
        width, height = pil_image.size
        num_pixels = int((width * height) * (self.damage / 400))  # 25% damage = ~6% of pixels
        
        # Make random pixels transparent
        for _ in range(num_pixels):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            draw.point((x, y), fill=(0, 0, 0, 0))  # Transparent
        
        # Convert back to Pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        
        # Create a new surface with alpha channel
        self.image = pygame.image.fromstring(data, size, mode).convert_alpha()


class Barrier:
    """A defensive barrier that the ship can hide behind."""
    def __init__(self, game, x_position):
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        
        # Set barrier dimensions
        self.width = 100
        self.height = 75
        self.color = (0, 255, 0)  # Green
        self.x = x_position
        self.y = game.screen.get_rect().height - 150  # Position above ship
        
        # Create a group to hold all barrier pieces
        self.pieces = Group()
        
        # Build the barrier
        self._build_barrier()
    
    def _build_barrier(self):
        """Build the barrier from individual pieces."""
        piece_width = 5
        piece_height = 5
        
        # Create grid of barrier pieces (except for a U-shaped gap)
        for row in range(self.height // piece_height):
            for col in range(self.width // piece_width):
                # Skip pieces to create a U-shaped gap at the bottom
                if (row >= self.height // piece_height - 4 and 
                    col >= self.width // piece_width // 3 and 
                    col < self.width // piece_width - self.width // piece_width // 3):
                    continue
                
                # Create the piece
                piece = BarrierPiece(
                    self,
                    self.x + col * piece_width,
                    self.y + row * piece_height,
                    piece_width,
                    piece_height,
                    self.color
                )
                self.pieces.add(piece)
    
    def update(self):
        """Update the state of the barrier."""
        pass  # No regular updates needed for static barriers
    
    def draw(self):
        """Draw the barrier on the screen."""
        self.pieces.draw(self.screen)
