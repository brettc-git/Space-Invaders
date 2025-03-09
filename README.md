# Space-Invaders

A Python implementation of the classic Space Invaders arcade game using Pygame.

## Collaborators
- Brett Chiu
- Jared Olalde (Team Leader)

## Game Features

- **Different Alien Types**: Four types of aliens (Pink, Blue, Green, Red) with different point values
- **UFO Special Enemy**: Appears randomly with varying point values
- **Animated Sprites**: All game entities feature animations
  - Aliens have two-frame movement animations and explosion animations
  - Ship has an 8-frame explosion animation
- **Defensive Barriers**: Destructible bunkers that protect the player
- **Dynamic Difficulty**: Game speeds up as aliens are destroyed
- **High Score System**: Tracks and saves top scores
- **Sound Effects**: Background music speeds up as aliens decrease, with sound effects for firing and explosions

## Controls

- **Arrow Keys**: Move ship (left/right/up/down)
- **Space**: Fire
- **P**: Start game (from launch screen)
- **ESC**: Quit game

## Game Screens

1. **Launch Screen**: Shows game title, alien point values, and menu options
2. **Game Screen**: Main gameplay area
3. **High Scores Screen**: Displays saved high scores

## Project Structure

- **space_invaders.py**: Main game class and entry point
- **settings.py**: Game configuration settings
- **ship.py**: Player ship implementation
- **aliens.py**: Implementation of all alien types and UFO
- **bullet.py**: Player and alien projectiles
- **barrier.py**: Destructible barriers implementation
- **scoreboard.py**: Score tracking and display

## Assets Used
- Main Ship: https://foozlecc.itch.io/void-main-ship
- All other assets created with pixel editors as required

## Requirements
- Python 3.x
- Pygame
- Pillow (Python Imaging Library)
