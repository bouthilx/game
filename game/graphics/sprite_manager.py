import pygame
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SpriteManager:
    """
    Singleton class for managing sprite loading, caching, and retrieval.
    Handles both individual sprites and sprite sheets.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._sprite_cache: Dict[str, pygame.Surface] = {}
            self._sprite_sheet_cache: Dict[str, List[pygame.Surface]] = {}
            self._default_sprite_size = (32, 32)
            self._assets_path = Path("assets/sprites")
            SpriteManager._initialized = True
    
    def set_assets_path(self, path: str):
        """Set the base path for sprite assets."""
        self._assets_path = Path(path)
    
    def load_sprite(self, path: str, size: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """
        Load a single sprite from file path.
        
        Args:
            path: Relative path from assets/sprites/ or absolute path
            size: Optional size to scale sprite to. If None, uses original size.
            
        Returns:
            pygame.Surface: Loaded sprite surface
        """
        cache_key = f"{path}_{size}" if size else path
        
        # Check cache first
        if cache_key in self._sprite_cache:
            return self._sprite_cache[cache_key]
        
        # Determine full path
        if os.path.isabs(path):
            full_path = Path(path)
        else:
            full_path = self._assets_path / path
        
        try:
            # Load sprite
            sprite = pygame.image.load(str(full_path))
            
            # Convert for better performance
            if sprite.get_alpha() is not None:
                sprite = sprite.convert_alpha()
            else:
                sprite = sprite.convert()
            
            # Scale if requested
            if size:
                sprite = pygame.transform.scale(sprite, size)
            
            # Cache and return
            self._sprite_cache[cache_key] = sprite
            return sprite
            
        except (pygame.error, FileNotFoundError) as e:
            # Create fallback sprite
            fallback_size = size or self._default_sprite_size
            fallback_sprite = self._create_fallback_sprite(fallback_size, path)
            self._sprite_cache[cache_key] = fallback_sprite
            print(f"Warning: Could not load sprite '{path}': {e}")
            return fallback_sprite
    
    def load_sprite_sheet(
        self, 
        path: str, 
        frame_size: Tuple[int, int],
        frames_per_row: Optional[int] = None,
        total_frames: Optional[int] = None
    ) -> List[pygame.Surface]:
        """
        Load a sprite sheet and split it into individual frames.
        
        Args:
            path: Path to sprite sheet file
            frame_size: Size of each frame (width, height)
            frames_per_row: Number of frames per row. If None, auto-calculate
            total_frames: Total number of frames to extract. If None, extract all
            
        Returns:
            List[pygame.Surface]: List of individual frame surfaces
        """
        cache_key = f"{path}_{frame_size}_{frames_per_row}_{total_frames}"
        
        # Check cache first
        if cache_key in self._sprite_sheet_cache:
            return self._sprite_sheet_cache[cache_key]
        
        # Load the sprite sheet
        sheet_surface = self.load_sprite(path)
        frames = []
        
        # Calculate dimensions
        sheet_width, sheet_height = sheet_surface.get_size()
        frame_width, frame_height = frame_size
        
        if frames_per_row is None:
            frames_per_row = sheet_width // frame_width
        
        rows = sheet_height // frame_height
        max_frames = frames_per_row * rows
        
        if total_frames is None:
            total_frames = max_frames
        else:
            total_frames = min(total_frames, max_frames)
        
        # Extract frames
        for i in range(total_frames):
            row = i // frames_per_row
            col = i % frames_per_row
            
            x = col * frame_width
            y = row * frame_height
            
            # Extract frame
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = pygame.Surface(frame_size, pygame.SRCALPHA)
            frame.blit(sheet_surface, (0, 0), frame_rect)
            
            frames.append(frame)
        
        # Cache and return
        self._sprite_sheet_cache[cache_key] = frames
        return frames
    
    def get_cached_sprite(self, cache_key: str) -> Optional[pygame.Surface]:
        """Get a sprite from cache without loading."""
        return self._sprite_cache.get(cache_key)
    
    def preload_sprites(self, sprite_paths: List[str], size: Optional[Tuple[int, int]] = None):
        """Preload a list of sprites into cache."""
        for path in sprite_paths:
            self.load_sprite(path, size)
    
    def clear_cache(self):
        """Clear all cached sprites."""
        self._sprite_cache.clear()
        self._sprite_sheet_cache.clear()
    
    def get_cache_info(self) -> Dict[str, int]:
        """Get information about current cache state."""
        return {
            "sprites_cached": len(self._sprite_cache),
            "sprite_sheets_cached": len(self._sprite_sheet_cache),
            "total_cached_items": len(self._sprite_cache) + len(self._sprite_sheet_cache)
        }
    
    def _create_fallback_sprite(self, size: Tuple[int, int], path: str) -> pygame.Surface:
        """Create a fallback sprite when loading fails."""
        sprite = pygame.Surface(size, pygame.SRCALPHA)
        
        # Create a distinctive pattern for fallback sprites
        sprite.fill((128, 0, 128))  # Purple background
        
        # Add an 'X' pattern
        width, height = size
        pygame.draw.line(sprite, (255, 255, 255), (0, 0), (width, height), 2)
        pygame.draw.line(sprite, (255, 255, 255), (width, 0), (0, height), 2)
        
        # Add border
        pygame.draw.rect(sprite, (255, 255, 255), sprite.get_rect(), 1)
        
        return sprite
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (mainly for testing)."""
        cls._instance = None
        cls._initialized = False