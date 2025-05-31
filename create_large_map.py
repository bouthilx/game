#!/usr/bin/env python3
import pygame

pygame.init()

# Créer une carte 2x plus grande
width, height = 64, 48  # Au lieu de 20x15, maintenant 64x48
tile_size = 1

surface = pygame.Surface((width, height))

# Définir les couleurs
grass = (34, 139, 34)
dirt = (139, 69, 19)
stone = (128, 128, 128)
wall = (165, 42, 42)
water = (0, 0, 255)
spawn = (255, 0, 0)

# Remplir de base avec de l'herbe
surface.fill(grass)

# Murs extérieurs
for x in range(width):
    surface.set_at((x, 0), wall)
    surface.set_at((x, height-1), wall)

for y in range(height):
    surface.set_at((0, y), wall)
    surface.set_at((width-1, y), wall)

# Zone de water (lac)
for x in range(15, 25):
    for y in range(10, 18):
        surface.set_at((x, y), water)

# Zone de stone (chemin)
for x in range(8, width-8):
    surface.set_at((x, height//2), stone)

# Quelques murs intérieurs (obstacles)
# Mur vertical
for y in range(8, 15):
    surface.set_at((35, y), wall)

# Mur horizontal
for x in range(40, 50):
    surface.set_at((x, 20), wall)

# Zone de dirt (chemins secondaires)
for y in range(height//2 - 2, height//2 + 3):
    for x in range(20, 30):
        surface.set_at((x, y), dirt)

# Point de spawn du joueur (centre-gauche)
surface.set_at((10, height//2), spawn)

# Sauvegarder la nouvelle carte
pygame.image.save(surface, "data/maps/large_map.png")
print(f"Large map created at data/maps/large_map.png ({width}x{height} pixels)")
print(f"Map size in tiles: {width}x{height} = {width*height} tiles")
print(f"Map size in world units: {width*32}x{height*32} = {width*32}x{height*32} pixels")

pygame.quit()