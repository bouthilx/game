from typing import List, Tuple

import pygame

from game.world.game_object import GameObject
from game.world.object_types import get_object_type, is_object_color
from game.world.tile_types import TileType, get_tile_type


class BitmapMap:
    def __init__(self, map_path: str, tile_size: int = 32):
        self.tile_size = tile_size
        self.map_surface = pygame.image.load(map_path)
        self.width = self.map_surface.get_width()
        self.height = self.map_surface.get_height()
        self.pixel_array = pygame.PixelArray(self.map_surface)

        self.spawn_point = self._find_spawn_point()
        self.objects = self._load_objects()
        self.object_collision_tiles = self._build_object_collision_map()

    def _find_spawn_point(self) -> Tuple[float, float]:
        spawn_tile_x, spawn_tile_y = None, None
        
        # First, find the red spawn marker
        for y in range(self.height):
            for x in range(self.width):
                color = self.map_surface.unmap_rgb(self.pixel_array[x, y])
                color_tuple = (
                    (color.r, color.g, color.b) if hasattr(color, "r") else color
                )
                if color_tuple == (255, 0, 0):
                    spawn_tile_x, spawn_tile_y = x, y
                    break
            if spawn_tile_x is not None:
                break
        
        # If no spawn marker found, use default
        if spawn_tile_x is None:
            spawn_tile_x, spawn_tile_y = 1, 1
        
        return self._find_walkable_spawn_near(spawn_tile_x, spawn_tile_y)
    
    def _find_walkable_spawn_near(self, tile_x: int, tile_y: int) -> Tuple[float, float]:
        """Find a walkable tile near the given spawn point."""
        # Try spawn point first
        world_x = tile_x * self.tile_size + self.tile_size // 2
        world_y = tile_y * self.tile_size + self.tile_size // 2
        
        # Note: We need to defer walkability check until after objects are loaded
        # For now, return the calculated position and check later
        return (world_x, world_y)
    
    def find_safe_spawn_position(self) -> Tuple[float, float]:
        """Find a safe spawn position after objects are loaded."""
        spawn_x, spawn_y = self.spawn_point
        spawn_tile_x = int(spawn_x // self.tile_size)
        spawn_tile_y = int(spawn_y // self.tile_size)
        
        # Check if current spawn is walkable for a player-sized rectangle
        if self.is_player_spawn_safe(spawn_x, spawn_y):
            return (spawn_x, spawn_y)
        
        # Search in expanding spiral around spawn point
        for radius in range(1, 10):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:  # Only check border of current radius
                        check_tile_x = spawn_tile_x + dx
                        check_tile_y = spawn_tile_y + dy
                        
                        if (0 <= check_tile_x < self.width and 0 <= check_tile_y < self.height):
                            check_x = check_tile_x * self.tile_size + self.tile_size // 2
                            check_y = check_tile_y * self.tile_size + self.tile_size // 2
                            
                            if self.is_player_spawn_safe(check_x, check_y):
                                return (check_x, check_y)
        
        # Fallback: return original spawn point
        return (spawn_x, spawn_y)
    
    def is_player_spawn_safe(self, x: float, y: float, player_width: int = 32, player_height: int = 32) -> bool:
        """Check if a player-sized rectangle can be safely placed at this position."""
        margin = 2
        corners = [
            (x + margin, y + margin),
            (x + player_width - margin, y + margin),
            (x + margin, y + player_height - margin),
            (x + player_width - margin, y + player_height - margin),
        ]
        
        for corner_x, corner_y in corners:
            if not self.is_walkable(corner_x, corner_y):
                return False
        return True

    def _load_objects(self) -> List[GameObject]:
        """Scan the map for object markers and create GameObjects."""
        objects = []
        
        for y in range(self.height):
            for x in range(self.width):
                color = self.map_surface.unmap_rgb(self.pixel_array[x, y])
                color_tuple = (
                    (color.r, color.g, color.b) if hasattr(color, "r") else color
                )
                
                # Check if this color represents an object
                object_type = get_object_type(color_tuple)
                if object_type:
                    # Calculate object position and size
                    obj_x = x * self.tile_size
                    obj_y = y * self.tile_size
                    obj_width = object_type.size[0] * self.tile_size
                    obj_height = object_type.size[1] * self.tile_size
                    
                    # Create GameObject
                    game_object = GameObject(
                        name=object_type.name,
                        x=obj_x,
                        y=obj_y,
                        width=obj_width,
                        height=obj_height,
                        sprite_path=object_type.sprite_path,
                        walkable=object_type.walkable,
                    )
                    
                    objects.append(game_object)
        
        return objects

    def _build_object_collision_map(self) -> set[Tuple[int, int]]:
        """Build a set of tile coordinates that have object collisions."""
        collision_tiles = set()
        
        for obj in self.objects:
            if not obj.walkable:
                tiles = obj.get_tile_coverage(self.tile_size)
                collision_tiles.update(tiles)
        
        return collision_tiles

    def get_tile_at_pixel(self, world_x: float, world_y: float) -> TileType:
        tile_x = int(world_x // self.tile_size)
        tile_y = int(world_y // self.tile_size)
        return self.get_tile_at_grid(tile_x, tile_y)

    def get_tile_at_grid(self, tile_x: int, tile_y: int) -> TileType:
        if tile_x < 0 or tile_y < 0 or tile_x >= self.width or tile_y >= self.height:
            return get_tile_type((0, 0, 0))

        color = self.map_surface.unmap_rgb(self.pixel_array[tile_x, tile_y])
        color_tuple = (color.r, color.g, color.b) if hasattr(color, "r") else color
        return get_tile_type(color_tuple)

    def is_walkable(self, world_x: float, world_y: float) -> bool:
        # Check terrain walkability
        if not self.get_tile_at_pixel(world_x, world_y).walkable:
            return False
        
        # Check object collisions
        tile_x = int(world_x // self.tile_size)
        tile_y = int(world_y // self.tile_size)
        
        if (tile_x, tile_y) in self.object_collision_tiles:
            return False
            
        return True

    def get_objects_at_point(self, world_x: float, world_y: float) -> List[GameObject]:
        """Get all objects that contain the given point."""
        objects_at_point = []
        for obj in self.objects:
            if obj.is_point_inside(world_x, world_y):
                objects_at_point.append(obj)
        return objects_at_point

    def get_objects_in_area(self, x: float, y: float, width: float, height: float) -> List[GameObject]:
        """Get all objects that intersect with the given area."""
        area_rect = pygame.Rect(int(x), int(y), int(width), int(height))
        intersecting_objects = []
        
        for obj in self.objects:
            if area_rect.colliderect(obj.rect):
                intersecting_objects.append(obj)
                
        return intersecting_objects

    def get_world_size(self) -> Tuple[int, int]:
        return (self.width * self.tile_size, self.height * self.tile_size)

    def render_terrain(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render only the terrain layer."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        start_tile_x = max(0, int(camera_x // self.tile_size))
        start_tile_y = max(0, int(camera_y // self.tile_size))
        end_tile_x = min(
            self.width, int((camera_x + screen_width) // self.tile_size) + 1
        )
        end_tile_y = min(
            self.height, int((camera_y + screen_height) // self.tile_size) + 1
        )

        # Render terrain tiles
        for tile_y in range(start_tile_y, end_tile_y):
            for tile_x in range(start_tile_x, end_tile_x):
                color = self.map_surface.unmap_rgb(self.pixel_array[tile_x, tile_y])
                color_tuple = (color.r, color.g, color.b) if hasattr(color, "r") else color
                
                # Skip object colors, render as terrain underneath
                if is_object_color(color_tuple):
                    # Render grass underneath objects
                    tile_type = get_tile_type((34, 139, 34))  # Grass
                else:
                    tile_type = get_tile_type(color_tuple)

                screen_x = tile_x * self.tile_size - camera_x
                screen_y = tile_y * self.tile_size - camera_y

                rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, tile_type.color, rect)

    def render_objects(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render only the objects layer."""
        for obj in self.objects:
            obj.render(screen, camera_x, camera_y)

    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render terrain and objects (for backward compatibility)."""
        self.render_terrain(screen, camera_x, camera_y)
        self.render_objects(screen, camera_x, camera_y)
