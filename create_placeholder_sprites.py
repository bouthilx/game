#!/usr/bin/env python3
"""Create placeholder sprite assets for testing."""

import pygame
import os

pygame.init()

# Create sprite directory
os.makedirs("assets/sprites", exist_ok=True)

# Define sprite data: (filename, size, color)
sprites = [
    # Trees and nature
    ("small_tree.png", (32, 32), (34, 139, 34)),  # Green
    ("large_tree.png", (64, 64), (0, 100, 0)),    # Dark green
    ("bush.png", (32, 32), (50, 205, 50)),        # Light green
    # Buildings  
    ("house.png", (96, 64), (139, 69, 19)),       # Brown
    ("shed.png", (64, 32), (160, 82, 45)),        # Saddle brown
    ("well.png", (32, 32), (105, 105, 105)),      # Dim gray
    # Interactive objects
    ("chest.png", (32, 32), (255, 215, 0)),       # Gold
    ("barrel.png", (32, 32), (139, 69, 19)),      # Brown
    # Infrastructure
    ("stone_wall.png", (32, 32), (128, 128, 128)), # Gray
    ("wooden_fence.png", (32, 32), (139, 69, 19)), # Brown
    ("bridge.png", (96, 32), (101, 67, 33)),      # Dark brown
]

for filename, size, color in sprites:
    surface = pygame.Surface(size)
    surface.fill(color)
    
    # Add a simple border to make objects more visible
    pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
    
    # Add some simple details based on object type
    if "tree" in filename:
        # Add trunk
        trunk_rect = pygame.Rect(size[0]//2 - 4, size[1] - 12, 8, 12)
        pygame.draw.rect(surface, (101, 67, 33), trunk_rect)
    elif "house" in filename:
        # Add door
        door_rect = pygame.Rect(size[0]//2 - 6, size[1] - 20, 12, 18)
        pygame.draw.rect(surface, (139, 69, 19), door_rect)
    elif "chest" in filename:
        # Add keyhole
        pygame.draw.circle(surface, (0, 0, 0), (size[0]//2, size[1]//2), 3)
    
    pygame.image.save(surface, f"assets/sprites/{filename}")
    print(f"Created {filename}")

print(f"Created {len(sprites)} placeholder sprites in assets/sprites/")
pygame.quit()