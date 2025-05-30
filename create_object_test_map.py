#!/usr/bin/env python3
"""Create a test map with objects to demonstrate the sprite system."""

import pygame

pygame.init()

width, height = 15, 10
surface = pygame.Surface((width, height))

# Base colors
grass = (34, 139, 34)
wall = (165, 42, 42)
water = (0, 0, 255)
spawn = (255, 0, 0)

# Object colors (from object_types.py)
small_tree = (50, 150, 50)
large_tree = (40, 120, 40)
house = (150, 75, 0)
shed = (120, 60, 0)
chest = (200, 200, 0)
stone_wall = (100, 100, 100)

# Fill with grass
surface.fill(grass)

# Create border walls
for x in range(width):
    surface.set_at((x, 0), wall)
    surface.set_at((x, height-1), wall)
for y in range(height):
    surface.set_at((0, y), wall)
    surface.set_at((width-1, y), wall)

# Add water pond
for x in range(3, 6):
    for y in range(6, 8):
        surface.set_at((x, y), water)

# Place objects:
# Spawn point
surface.set_at((2, 2), spawn)

# Trees scattered around
surface.set_at((5, 2), small_tree)
surface.set_at((8, 1), small_tree)
surface.set_at((11, 3), large_tree)  # 2x2 large tree
surface.set_at((7, 6), small_tree)

# Buildings
surface.set_at((9, 6), house)     # 3x2 house
surface.set_at((3, 3), shed)      # 2x1 shed

# Interactive objects
surface.set_at((12, 8), chest)    # Treasure chest

# Stone walls to create barriers
surface.set_at((6, 4), stone_wall)
surface.set_at((7, 4), stone_wall)
surface.set_at((8, 4), stone_wall)

# Save the map
pygame.image.save(surface, "data/maps/object_test_map.png")
print("Object test map created at data/maps/object_test_map.png")

# Print legend
print("\nMap Legend:")
print("- Green: Grass (walkable)")
print("- Brown: Walls (impassable)")
print("- Blue: Water (impassable)")
print("- Red: Player spawn")
print("- Light Green: Small trees (impassable)")
print("- Dark Green: Large tree 2x2 (impassable)")
print("- Brown (dark): House 3x2 (impassable)")
print("- Brown (medium): Shed 2x1 (impassable)")
print("- Yellow: Chest (walkable)")
print("- Gray: Stone walls (impassable)")

pygame.quit()