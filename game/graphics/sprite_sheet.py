import pygame
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import json

from .sprite_manager import SpriteManager
from .animation import Animation, AnimationMode


class SpriteSheet:
    """
    Utility class for loading and parsing sprite sheets with metadata.
    Supports JSON configuration files for complex sprite sheet layouts.
    """
    
    def __init__(self, sprite_manager: Optional[SpriteManager] = None):
        self.sprite_manager = sprite_manager or SpriteManager()
        self.sheet_surface: Optional[pygame.Surface] = None
        self.metadata: Dict = {}
    
    def load_from_file(
        self, 
        sheet_path: str, 
        frame_size: Tuple[int, int],
        frames_per_row: Optional[int] = None
    ) -> List[pygame.Surface]:
        """
        Load sprite sheet from file with uniform frame size.
        
        Args:
            sheet_path: Path to sprite sheet image
            frame_size: Size of each frame (width, height)
            frames_per_row: Number of frames per row
            
        Returns:
            List[pygame.Surface]: List of extracted frames
        """
        return self.sprite_manager.load_sprite_sheet(
            sheet_path, frame_size, frames_per_row
        )
    
    def load_from_config(self, config_path: str) -> Dict[str, List[pygame.Surface]]:
        """
        Load sprite sheet using JSON configuration file.
        
        Config format:
        {
            "image": "path/to/spritesheet.png",
            "frame_size": [32, 32],
            "animations": {
                "idle": {
                    "frames": [0, 1, 2, 3],
                    "row": 0
                },
                "walk": {
                    "frames": [0, 1, 2, 3],
                    "row": 1
                }
            }
        }
        
        Args:
            config_path: Path to JSON configuration file
            
        Returns:
            Dict[str, List[pygame.Surface]]: Dictionary of animation name to frames
        """
        config_file = Path(config_path)
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not load sprite sheet config '{config_path}': {e}")
        
        self.metadata = config
        
        # Load the main sprite sheet
        image_path = config.get("image", "")
        if not image_path:
            raise ValueError("Config must specify 'image' path")
        
        # Make path relative to config file location
        if not Path(image_path).is_absolute():
            image_path = str(config_file.parent / image_path)
        
        frame_size = tuple(config.get("frame_size", [32, 32]))
        self.sheet_surface = self.sprite_manager.load_sprite(image_path)
        
        # Extract animations
        animations = {}
        animation_configs = config.get("animations", {})
        
        for anim_name, anim_config in animation_configs.items():
            frames = self._extract_frames_from_config(anim_config, frame_size)
            animations[anim_name] = frames
        
        return animations
    
    def create_animations_from_config(self, config_path: str) -> Dict[str, Animation]:
        """
        Create Animation objects from configuration file.
        
        Args:
            config_path: Path to JSON configuration file
            
        Returns:
            Dict[str, Animation]: Dictionary of animation name to Animation object
        """
        frame_dict = self.load_from_config(config_path)
        animations = {}
        
        animation_configs = self.metadata.get("animations", {})
        
        for anim_name, frames in frame_dict.items():
            anim_config = animation_configs.get(anim_name, {})
            
            # Get animation settings
            frame_duration = anim_config.get("frame_duration", 0.1)
            mode_str = anim_config.get("mode", "loop")
            
            # Convert mode string to enum
            mode = AnimationMode.LOOP
            if mode_str == "once":
                mode = AnimationMode.ONCE
            elif mode_str == "ping_pong":
                mode = AnimationMode.PING_PONG
            
            animations[anim_name] = Animation(
                frames=frames,
                frame_duration=frame_duration,
                mode=mode,
                name=anim_name
            )
        
        return animations
    
    def create_directional_animations(
        self,
        sheet_path: str,
        frame_size: Tuple[int, int],
        directions: List[str] = None,
        frames_per_direction: int = 4,
        frame_duration: float = 0.1
    ) -> Dict[str, Animation]:
        """
        Create directional animations from a sprite sheet organized by direction.
        
        Expected layout:
        Row 0: down_idle, down_walk
        Row 1: up_idle, up_walk  
        Row 2: left_idle, left_walk
        Row 3: right_idle, right_walk
        
        Args:
            sheet_path: Path to sprite sheet
            frame_size: Size of each frame
            directions: List of direction names (default: ["down", "up", "left", "right"])
            frames_per_direction: Number of frames per direction
            frame_duration: Duration of each frame
            
        Returns:
            Dict[str, Animation]: Dictionary of direction to Animation
        """
        if directions is None:
            directions = ["down", "up", "left", "right"]
        
        all_frames = self.load_from_file(sheet_path, frame_size, frames_per_direction)
        animations = {}
        
        for i, direction in enumerate(directions):
            start_idx = i * frames_per_direction
            end_idx = start_idx + frames_per_direction
            
            if start_idx < len(all_frames):
                # Take as many frames as available, up to frames_per_direction
                actual_end = min(end_idx, len(all_frames))
                direction_frames = all_frames[start_idx:actual_end]
                
                if direction_frames:  # Only create animation if we have frames
                    animations[direction] = Animation(
                        frames=direction_frames,
                        frame_duration=frame_duration,
                        mode=AnimationMode.LOOP,
                        name=f"{direction}_walk"
                    )
        
        return animations
    
    def _extract_frames_from_config(
        self, 
        anim_config: Dict, 
        frame_size: Tuple[int, int]
    ) -> List[pygame.Surface]:
        """Extract frames based on animation configuration."""
        if not self.sheet_surface:
            raise ValueError("No sprite sheet loaded")
        
        frames = []
        frame_indices = anim_config.get("frames", [])
        row = anim_config.get("row", 0)
        
        frame_width, frame_height = frame_size
        sheet_width = self.sheet_surface.get_width()
        frames_per_row = sheet_width // frame_width
        
        for frame_idx in frame_indices:
            # Calculate position in sprite sheet
            col = frame_idx
            x = col * frame_width
            y = row * frame_height
            
            # Extract frame
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = pygame.Surface(frame_size, pygame.SRCALPHA)
            frame.blit(self.sheet_surface, (0, 0), frame_rect)
            
            frames.append(frame)
        
        return frames
    
    @staticmethod
    def create_config_template(
        output_path: str,
        image_path: str,
        frame_size: Tuple[int, int] = (32, 32),
        animation_names: List[str] = None
    ):
        """
        Create a template configuration file for a sprite sheet.
        
        Args:
            output_path: Where to save the config file
            image_path: Path to the sprite sheet image
            frame_size: Size of each frame
            animation_names: List of animation names to include
        """
        if animation_names is None:
            animation_names = ["idle", "walk", "attack"]
        
        config = {
            "image": image_path,
            "frame_size": list(frame_size),
            "animations": {}
        }
        
        for i, anim_name in enumerate(animation_names):
            config["animations"][anim_name] = {
                "frames": [0, 1, 2, 3],
                "row": i,
                "frame_duration": 0.1,
                "mode": "loop"
            }
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Created sprite sheet config template at: {output_path}")


class CharacterSpriteSheet:
    """
    Specialized sprite sheet loader for character sprites with standard directions.
    """
    
    def __init__(self, sprite_manager: Optional[SpriteManager] = None):
        self.sprite_sheet = SpriteSheet(sprite_manager)
    
    def load_character_animations(
        self,
        sheet_path: str,
        frame_size: Tuple[int, int] = (32, 32),
        animation_types: List[str] = None
    ) -> Dict[str, Dict[str, Animation]]:
        """
        Load character animations organized by type and direction.
        
        Expected sheet layout:
        - Each row represents a direction: down, up, left, right
        - Each column represents an animation type: idle, walk, attack
        
        Args:
            sheet_path: Path to character sprite sheet
            frame_size: Size of each frame
            animation_types: Types of animations (default: ["idle", "walk"])
            
        Returns:
            Dict[str, Dict[str, Animation]]: 
            {
                "idle": {"down": Animation, "up": Animation, ...},
                "walk": {"down": Animation, "up": Animation, ...}
            }
        """
        if animation_types is None:
            animation_types = ["idle", "walk"]
        
        directions = ["down", "up", "left", "right"]
        frames_per_animation = 4  # Standard 4 frames per animation
        
        all_frames = self.sprite_sheet.load_from_file(
            sheet_path, frame_size, len(animation_types) * frames_per_animation
        )
        
        animations = {}
        
        for anim_idx, anim_type in enumerate(animation_types):
            animations[anim_type] = {}
            
            for dir_idx, direction in enumerate(directions):
                # Calculate frame indices for this animation and direction
                row_start = dir_idx * len(animation_types) * frames_per_animation
                anim_start = row_start + anim_idx * frames_per_animation
                anim_end = anim_start + frames_per_animation
                
                if anim_start < len(all_frames):
                    # Take as many frames as available
                    actual_end = min(anim_end, len(all_frames))
                    anim_frames = all_frames[anim_start:actual_end]
                    
                    if anim_frames:  # Only create animation if we have frames
                        # Determine animation mode
                        mode = AnimationMode.LOOP if anim_type != "attack" else AnimationMode.ONCE
                        
                        animations[anim_type][direction] = Animation(
                            frames=anim_frames,
                            frame_duration=0.15 if anim_type == "walk" else 0.1,
                            mode=mode,
                            name=f"{anim_type}_{direction}"
                        )
        
        return animations