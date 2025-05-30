#!/usr/bin/env python3
import pygame

pygame.init()

width, height = 20, 15
tile_size = 1

surface = pygame.Surface((width, height))

grass = (34, 139, 34)
wall = (165, 42, 42)
water = (0, 0, 255)
spawn = (255, 0, 0)
chest = (255, 255, 0)

surface.fill(grass)

for x in range(width):
    surface.set_at((x, 0), wall)
    surface.set_at((x, height-1), wall)

for y in range(height):
    surface.set_at((0, y), wall)
    surface.set_at((width-1, y), wall)

for x in range(5, 8):
    for y in range(3, 6):
        surface.set_at((x, y), water)

for x in range(12, 15):
    for y in range(8, 11):
        surface.set_at((x, y), wall)

surface.set_at((2, 2), spawn)
surface.set_at((17, 12), chest)

pygame.image.save(surface, "data/maps/test_map.png")
print("Sample map created at data/maps/test_map.png")

pygame.quit()