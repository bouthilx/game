from typing import Tuple
import pygame


class GameObject:
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        width: int,
        height: int,
        sprite_path: str = None,
        walkable: bool = False,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.width = width  # Width in pixels
        self.height = height  # Height in pixels
        self.sprite_path = sprite_path
        self.walkable = walkable
        self.sprite_surface = None

        if sprite_path:
            try:
                self.sprite_surface = pygame.image.load(sprite_path)
                # Scale sprite to match object size
                self.sprite_surface = pygame.transform.scale(
                    self.sprite_surface, (width, height)
                )
            except pygame.error:
                # If sprite loading fails, create a colored rectangle
                self.sprite_surface = pygame.Surface((width, height))
                self.sprite_surface.fill((100, 100, 100))  # Gray fallback

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def get_tile_coverage(self, tile_size: int) -> list[Tuple[int, int]]:
        """Get list of tile coordinates this object covers."""
        tiles = []
        start_tile_x = int(self.x // tile_size)
        start_tile_y = int(self.y // tile_size)
        end_tile_x = int((self.x + self.width - 1) // tile_size)
        end_tile_y = int((self.y + self.height - 1) // tile_size)

        for tile_y in range(start_tile_y, end_tile_y + 1):
            for tile_x in range(start_tile_x, end_tile_x + 1):
                tiles.append((tile_x, tile_y))

        return tiles

    def is_point_inside(self, x: float, y: float) -> bool:
        """Check if a point is inside this object."""
        return self.rect.collidepoint(int(x), int(y))

    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Render the object sprite."""
        if self.sprite_surface:
            screen_x = self.x - camera_x
            screen_y = self.y - camera_y
            screen.blit(self.sprite_surface, (screen_x, screen_y))