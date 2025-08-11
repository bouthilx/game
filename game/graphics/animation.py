import pygame
from typing import List, Optional
from enum import Enum


class AnimationMode(Enum):
    """Animation playback modes."""
    LOOP = "loop"           # Continuous looping
    ONCE = "once"           # Play once and stop
    PING_PONG = "ping_pong" # Play forward then backward


class Animation:
    """
    Handles sprite animation with multiple frames and timing.
    """
    
    def __init__(
        self,
        frames: List[pygame.Surface],
        frame_duration: float = 0.1,
        mode: AnimationMode = AnimationMode.LOOP,
        name: str = ""
    ):
        """
        Initialize animation.
        
        Args:
            frames: List of sprite frames
            frame_duration: Duration of each frame in seconds
            mode: Animation playback mode
            name: Optional name for debugging
        """
        if not frames:
            raise ValueError("Animation must have at least one frame")
        
        self.frames = frames
        self.frame_duration = frame_duration
        self.mode = mode
        self.name = name
        
        # Animation state
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.is_playing = True
        self.is_finished = False
        self.direction = 1  # 1 for forward, -1 for backward (ping-pong mode)
    
    def update(self, dt: float) -> pygame.Surface:
        """
        Update animation and return current frame.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            pygame.Surface: Current frame surface
        """
        if not self.is_playing or self.is_finished:
            return self.frames[self.current_frame_index]
        
        self.elapsed_time += dt
        
        # Check if we should advance to next frame
        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time = 0.0
            self._advance_frame()
        
        return self.frames[self.current_frame_index]
    
    def _advance_frame(self):
        """Advance to next frame based on animation mode."""
        if self.mode == AnimationMode.LOOP:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            
        elif self.mode == AnimationMode.ONCE:
            if self.current_frame_index < len(self.frames) - 1:
                self.current_frame_index += 1
            else:
                self.is_finished = True
                
        elif self.mode == AnimationMode.PING_PONG:
            # Move in current direction
            next_index = self.current_frame_index + self.direction
            
            # Check boundaries and reverse direction if needed
            if next_index >= len(self.frames):
                self.direction = -1
                self.current_frame_index = len(self.frames) - 2
            elif next_index < 0:
                self.direction = 1
                self.current_frame_index = 1
            else:
                self.current_frame_index = next_index
    
    def play(self):
        """Start or resume animation."""
        self.is_playing = True
    
    def pause(self):
        """Pause animation."""
        self.is_playing = False
    
    def stop(self):
        """Stop animation and reset to first frame."""
        self.is_playing = False
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.is_finished = False
        self.direction = 1
    
    def reset(self):
        """Reset animation to beginning without stopping."""
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.is_finished = False
        self.direction = 1
    
    def get_current_frame(self) -> pygame.Surface:
        """Get current frame without updating."""
        return self.frames[self.current_frame_index]
    
    def set_frame(self, frame_index: int):
        """Set current frame index."""
        if 0 <= frame_index < len(self.frames):
            self.current_frame_index = frame_index
            self.elapsed_time = 0.0
    
    def get_total_duration(self) -> float:
        """Get total duration of one animation cycle."""
        if self.mode == AnimationMode.PING_PONG:
            return (len(self.frames) * 2 - 2) * self.frame_duration
        else:
            return len(self.frames) * self.frame_duration
    
    def copy(self) -> 'Animation':
        """Create a copy of this animation."""
        return Animation(
            frames=self.frames.copy(),
            frame_duration=self.frame_duration,
            mode=self.mode,
            name=self.name
        )
    
    @property
    def frame_count(self) -> int:
        """Get number of frames in animation."""
        return len(self.frames)
    
    @property
    def progress(self) -> float:
        """Get animation progress as a value between 0.0 and 1.0."""
        if not self.frames:
            return 0.0
        
        # Calculate progress based on current frame and elapsed time within frame
        frame_progress = self.current_frame_index / len(self.frames)
        time_progress_within_frame = (self.elapsed_time / self.frame_duration) / len(self.frames)
        
        return min(1.0, frame_progress + time_progress_within_frame)


class AnimationSet:
    """
    Manages a set of named animations for an entity.
    """
    
    def __init__(self):
        self.animations: dict[str, Animation] = {}
        self.current_animation: Optional[str] = None
        self.fallback_animation: Optional[str] = None
    
    def add_animation(self, name: str, animation: Animation):
        """Add an animation to the set."""
        self.animations[name] = animation
        
        # Set as current if it's the first animation
        if self.current_animation is None:
            self.current_animation = name
    
    def play_animation(self, name: str, restart: bool = True) -> bool:
        """
        Play a specific animation.
        
        Args:
            name: Name of animation to play
            restart: Whether to restart if animation is already playing
            
        Returns:
            bool: True if animation was found and started
        """
        if name not in self.animations:
            return False
        
        # Don't restart if already playing the same animation
        if not restart and self.current_animation == name:
            return True
        
        self.current_animation = name
        if restart:
            self.animations[name].reset()
        self.animations[name].play()
        
        return True
    
    def update(self, dt: float) -> Optional[pygame.Surface]:
        """Update current animation and return current frame."""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].update(dt)
        elif self.fallback_animation and self.fallback_animation in self.animations:
            return self.animations[self.fallback_animation].update(dt)
        return None
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Get current frame without updating."""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].get_current_frame()
        elif self.fallback_animation and self.fallback_animation in self.animations:
            return self.animations[self.fallback_animation].get_current_frame()
        return None
    
    def set_fallback_animation(self, name: str):
        """Set fallback animation to use when current animation is not available."""
        if name in self.animations:
            self.fallback_animation = name
    
    def has_animation(self, name: str) -> bool:
        """Check if animation exists."""
        return name in self.animations
    
    def get_animation_names(self) -> List[str]:
        """Get list of all animation names."""
        return list(self.animations.keys())
    
    def is_current_animation_finished(self) -> bool:
        """Check if current animation has finished (for ONCE mode animations)."""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].is_finished
        return False