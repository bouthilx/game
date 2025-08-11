import pygame
from typing import Dict, Optional
from enum import Enum

from .entity import Entity
from game.graphics.sprite_manager import SpriteManager
from game.graphics.animation import AnimationSet
from game.graphics.sprite_sheet import CharacterSpriteSheet, SpriteSheet


class AnimationState(Enum):
    """Common animation states for entities."""
    IDLE = "idle"
    WALK = "walk"
    ATTACK = "attack"
    HURT = "hurt"
    DEATH = "death"


class AnimatedEntity(Entity):
    """
    Enhanced Entity class with sprite and animation support.
    Provides a foundation for all animated game entities.
    """
    
    def __init__(
        self, 
        x: float = 0, 
        y: float = 0, 
        width: int = 32, 
        height: int = 32,
        sprite_sheet_path: Optional[str] = None,
        fallback_color: tuple[int, int, int] = (128, 128, 128)
    ):
        super().__init__(x, y, width, height)
        
        # Graphics system
        self.sprite_manager = SpriteManager()
        self.animation_set = AnimationSet()
        self.sprite_sheet_path = sprite_sheet_path
        self.fallback_color = fallback_color
        
        # Animation state
        self.facing_direction = "down"  # down, up, left, right
        self.animation_state = AnimationState.IDLE
        self.last_animation_state = None
        self.last_facing_direction = None
        
        # Load sprites if path provided
        if sprite_sheet_path:
            self._load_character_sprites()
        
        # Ensure we have a fallback animation
        if not self.animation_set.animations:
            self._create_fallback_animation()
    
    def _load_character_sprites(self):
        """Load character sprites from sprite sheet."""
        if not self.sprite_sheet_path:
            return
        
        try:
            # Standard character sprite loading (works for all characters)
            character_sheet = CharacterSpriteSheet(self.sprite_manager)
            
            # For goblins and ogres, include death animations
            if "goblin" in self.sprite_sheet_path or "ogre" in self.sprite_sheet_path:
                animation_types = ["idle", "walk", "attack", "death"]
            else:
                animation_types = ["idle", "walk", "attack"]
            
            animations = character_sheet.load_character_animations(
                self.sprite_sheet_path,
                (self.width, self.height),
                animation_types
            )
            
            # Add all animations to the set
            for anim_type, directions in animations.items():
                for direction, animation in directions.items():
                    anim_name = f"{anim_type}_{direction}"
                    self.animation_set.add_animation(anim_name, animation)
            
            # Set fallback to idle_down if available
            if self.animation_set.has_animation("idle_down"):
                self.animation_set.set_fallback_animation("idle_down")
            
        except Exception as e:
            print(f"Warning: Could not load character sprites from '{self.sprite_sheet_path}': {e}")
            self._create_fallback_animation()
    
    def _create_fallback_animation(self):
        """Create a basic fallback animation using colored rectangles."""
        from game.graphics.animation import Animation, AnimationMode
        
        # Create simple colored rectangle frames
        frames = []
        for i in range(2):  # Simple 2-frame animation
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Alternate brightness for animation effect
            brightness = 255 if i == 0 else 200
            color = tuple(min(255, max(0, c * brightness // 255)) for c in self.fallback_color)
            
            frame.fill(color)
            
            # Add border
            pygame.draw.rect(frame, (255, 255, 255), frame.get_rect(), 1)
            
            frames.append(frame)
        
        # Create fallback animation
        fallback_anim = Animation(frames, frame_duration=0.5, mode=AnimationMode.LOOP, name="fallback")
        self.animation_set.add_animation("fallback", fallback_anim)
        self.animation_set.set_fallback_animation("fallback")
    
    def set_animation_state(self, state: AnimationState, force: bool = False):
        """
        Set the current animation state.
        
        Args:
            state: New animation state
            force: Force state change even if already in this state
        """
        if not force and self.animation_state == state:
            return
        
        # Log animation state changes for debugging
        if hasattr(self, '_debug_id'):  # Only for enemies we're tracking
            print(f"ANIM: Entity {self._debug_id} changing from {self.animation_state.value} to {state.value}")
        
        self.last_animation_state = self.animation_state
        self.animation_state = state
        self._update_animation()
    
    def set_facing_direction(self, direction: str, force: bool = False):
        """
        Set the facing direction.
        
        Args:
            direction: New direction ("down", "up", "left", "right")
            force: Force direction change even if already facing this direction
        """
        if direction not in ["down", "up", "left", "right"]:
            return
        
        if not force and self.facing_direction == direction:
            return
        
        self.last_facing_direction = self.facing_direction
        self.facing_direction = direction
        self._update_animation()
    
    def _update_animation(self):
        """Update current animation based on state and direction."""
        animation_name = f"{self.animation_state.value}_{self.facing_direction}"
        
        # For attack and death animations, don't restart if already playing
        restart = self.animation_state not in [AnimationState.ATTACK, AnimationState.DEATH]
        
        # Try to play the specific animation
        if not self.animation_set.play_animation(animation_name, restart=restart):
            # Fallback to just the state if direction-specific doesn't exist
            if not self.animation_set.play_animation(self.animation_state.value, restart=restart):
                # Ultimate fallback (but not for death animations)
                if self.animation_state != AnimationState.DEATH:
                    if not self.animation_set.play_animation("idle_down", restart=restart):
                        self.animation_set.play_animation("fallback", restart=restart)
    
    def update_animation(self, dt: float) -> Optional[pygame.Surface]:
        """
        Update animation and return current frame.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            Current animation frame
        """
        return self.animation_set.update(dt)
    
    def get_current_sprite(self) -> Optional[pygame.Surface]:
        """Get current sprite frame without updating animation."""
        return self.animation_set.get_current_frame()
    
    def update_movement_animation(self, velocity_x: float, velocity_y: float):
        """
        Update animation based on movement velocity.
        Automatically sets walking/idle state and facing direction.
        
        Args:
            velocity_x: Horizontal velocity
            velocity_y: Vertical velocity
        """
        # Don't override special animations (attack, death, hurt)
        if self.animation_state in [AnimationState.ATTACK, AnimationState.DEATH, AnimationState.HURT]:
            # Log attempts to override death animation
            if self.animation_state == AnimationState.DEATH and (abs(velocity_x) > 0.1 or abs(velocity_y) > 0.1):
                print(f"ANIM: Blocked movement animation override on DEATH state (vel: {velocity_x:.1f}, {velocity_y:.1f})")
            return
        
        # Determine if moving
        is_moving = abs(velocity_x) > 0.1 or abs(velocity_y) > 0.1
        
        # Set animation state
        if is_moving and self.animation_state == AnimationState.IDLE:
            self.set_animation_state(AnimationState.WALK)
        elif not is_moving and self.animation_state == AnimationState.WALK:
            self.set_animation_state(AnimationState.IDLE)
        
        # Determine facing direction based on movement
        if is_moving:
            # Prioritize horizontal movement for direction
            if abs(velocity_x) > abs(velocity_y):
                direction = "right" if velocity_x > 0 else "left"
            else:
                direction = "down" if velocity_y > 0 else "up"
            
            self.set_facing_direction(direction)
    
    def play_attack_animation(self):
        """Play attack animation once."""
        self.set_animation_state(AnimationState.ATTACK, force=True)
        # Force restart the animation to play from beginning
        animation_name = f"{AnimationState.ATTACK.value}_{self.facing_direction}"
        self.animation_set.play_animation(animation_name, restart=True)
    
    def play_death_animation(self):
        """Play death animation once."""
        self.set_animation_state(AnimationState.DEATH, force=True)
        # Force restart the animation to play from beginning
        animation_name = f"{AnimationState.DEATH.value}_{self.facing_direction}"
        self.animation_set.play_animation(animation_name, restart=True)
    
    def is_attack_animation_finished(self) -> bool:
        """Check if attack animation has finished."""
        return (self.animation_state == AnimationState.ATTACK and 
                self.animation_set.is_current_animation_finished())
    
    def is_death_animation_finished(self) -> bool:
        """Check if death animation has finished."""
        return (self.animation_state == AnimationState.DEATH and 
                self.animation_set.is_current_animation_finished())
    
    def render(self, screen: pygame.Surface):
        """
        Render the animated entity.
        
        Args:
            screen: Surface to render on
        """
        # Get current sprite frame
        sprite = self.get_current_sprite()
        
        if sprite:
            # Render sprite
            screen.blit(sprite, (self.x, self.y))
        else:
            # Fallback to colored rectangle
            pygame.draw.rect(screen, self.fallback_color, self.rect)
    
    def update(self, dt: float):
        """
        Update the animated entity.
        
        Args:
            dt: Delta time in seconds
        """
        # Update base entity
        super().update(dt)
        
        # Update animations
        self.update_animation(dt)
        
        # Auto-transition from attack back to idle
        if self.is_attack_animation_finished():
            self.set_animation_state(AnimationState.IDLE)
        
        # Death animation stays on death (no transition back)
    
    def has_animation(self, animation_name: str) -> bool:
        """Check if entity has a specific animation."""
        return self.animation_set.has_animation(animation_name)
    
    def get_animation_info(self) -> Dict[str, any]:
        """Get information about current animation state."""
        return {
            "current_state": self.animation_state.value,
            "facing_direction": self.facing_direction,
            "current_animation": self.animation_set.current_animation,
            "available_animations": self.animation_set.get_animation_names(),
            "has_sprites": len(self.animation_set.animations) > 1,  # More than just fallback
            "sprite_sheet_path": self.sprite_sheet_path
        }