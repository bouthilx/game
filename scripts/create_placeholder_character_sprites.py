#!/usr/bin/env python3
"""
Script to create placeholder character sprites for testing the sprite system.
Creates simple colored rectangles with directional indicators.
"""

import pygame
import os
from pathlib import Path

def create_placeholder_character_sprite(
    size: tuple[int, int],
    base_color: tuple[int, int, int],
    direction: str,
    animation_type: str,
    frame_number: int = 0
) -> pygame.Surface:
    """Create a placeholder sprite with color and direction indicators."""
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    
    # Base character color
    character_rect = pygame.Rect(2, 2, width-4, height-4)
    pygame.draw.rect(surface, base_color, character_rect)
    
    # Direction indicator
    direction_colors = {
        "down": (255, 255, 255),   # White
        "up": (255, 255, 0),       # Yellow  
        "left": (0, 255, 255),     # Cyan
        "right": (255, 0, 255)     # Magenta
    }
    
    # Draw direction indicator (small triangle)
    center_x, center_y = width // 2, height // 2
    triangle_size = 4
    
    direction_color = direction_colors.get(direction, (255, 255, 255))
    
    if direction == "down":
        points = [
            (center_x, center_y + triangle_size),
            (center_x - triangle_size, center_y - triangle_size),
            (center_x + triangle_size, center_y - triangle_size)
        ]
    elif direction == "up":
        points = [
            (center_x, center_y - triangle_size),
            (center_x - triangle_size, center_y + triangle_size),
            (center_x + triangle_size, center_y + triangle_size)
        ]
    elif direction == "left":
        points = [
            (center_x - triangle_size, center_y),
            (center_x + triangle_size, center_y - triangle_size),
            (center_x + triangle_size, center_y + triangle_size)
        ]
    else:  # right
        points = [
            (center_x + triangle_size, center_y),
            (center_x - triangle_size, center_y - triangle_size),
            (center_x - triangle_size, center_y + triangle_size)
        ]
    
    pygame.draw.polygon(surface, direction_color, points)
    
    # Animation frame indicator (small dots)
    if animation_type in ["walk", "attack"]:
        dot_y = height - 6
        for i in range(4):  # 4 frames max
            dot_x = 6 + i * 6
            dot_color = (255, 255, 255) if i == frame_number else (128, 128, 128)
            pygame.draw.circle(surface, dot_color, (dot_x, dot_y), 2)
    
    # Border
    pygame.draw.rect(surface, (50, 50, 50), surface.get_rect(), 1)
    
    return surface

def create_character_sprite_sheet(
    character_name: str,
    size: tuple[int, int],
    base_color: tuple[int, int, int],
    output_path: str
):
    """Create a complete character sprite sheet."""
    # Create sprite sheet surface
    # Layout: 4 rows (directions) x 12 columns (3 animations x 4 frames)
    sheet_width = 12 * size[0]
    sheet_height = 4 * size[1]
    sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    
    directions = ["down", "up", "left", "right"]
    animations = ["idle", "walk", "attack"]
    
    for row, direction in enumerate(directions):
        for anim_idx, animation in enumerate(animations):
            for frame in range(4):
                sprite = create_placeholder_character_sprite(
                    size, base_color, direction, animation, frame
                )
                
                x = (anim_idx * 4 + frame) * size[0]
                y = row * size[1]
                sheet.blit(sprite, (x, y))
    
    # Save sprite sheet
    pygame.image.save(sheet, output_path)
    print(f"Created {character_name} sprite sheet: {output_path}")

def create_sprite_config(character_name: str, output_path: str):
    """Create a JSON config file for the character sprite sheet."""
    config = {
        "image": f"{character_name}_spritesheet.png",
        "frame_size": [32, 32],
        "animations": {
            "idle_down": {"frames": [0, 1, 2, 3], "row": 0, "frame_duration": 0.2, "mode": "loop"},
            "idle_up": {"frames": [0, 1, 2, 3], "row": 1, "frame_duration": 0.2, "mode": "loop"},
            "idle_left": {"frames": [0, 1, 2, 3], "row": 2, "frame_duration": 0.2, "mode": "loop"},
            "idle_right": {"frames": [0, 1, 2, 3], "row": 3, "frame_duration": 0.2, "mode": "loop"},
            
            "walk_down": {"frames": [4, 5, 6, 7], "row": 0, "frame_duration": 0.15, "mode": "loop"},
            "walk_up": {"frames": [4, 5, 6, 7], "row": 1, "frame_duration": 0.15, "mode": "loop"},
            "walk_left": {"frames": [4, 5, 6, 7], "row": 2, "frame_duration": 0.15, "mode": "loop"},
            "walk_right": {"frames": [4, 5, 6, 7], "row": 3, "frame_duration": 0.15, "mode": "loop"},
            
            "attack_down": {"frames": [8, 9, 10, 11], "row": 0, "frame_duration": 0.1, "mode": "once"},
            "attack_up": {"frames": [8, 9, 10, 11], "row": 1, "frame_duration": 0.1, "mode": "once"},
            "attack_left": {"frames": [8, 9, 10, 11], "row": 2, "frame_duration": 0.1, "mode": "once"},
            "attack_right": {"frames": [8, 9, 10, 11], "row": 3, "frame_duration": 0.1, "mode": "once"}
        }
    }
    
    import json
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created {character_name} config: {output_path}")

def main():
    pygame.init()
    
    # Character definitions
    characters = [
        ("player", (32, 32), (0, 100, 200)),      # Blue player
        ("goblin", (32, 32), (100, 200, 100)),    # Green goblin
        ("ogre", (64, 64), (200, 100, 100))       # Red ogre (larger)
    ]
    
    # Create sprites directory
    sprites_dir = Path("assets/sprites/characters")
    sprites_dir.mkdir(parents=True, exist_ok=True)
    
    for character_name, size, color in characters:
        # Create sprite sheet
        sheet_path = sprites_dir / f"{character_name}_spritesheet.png"
        create_character_sprite_sheet(character_name, size, color, str(sheet_path))
        
        # Create config file
        config_path = sprites_dir / f"{character_name}_config.json"
        create_sprite_config(character_name, str(config_path))
    
    print("All placeholder character sprites created!")

if __name__ == "__main__":
    main()