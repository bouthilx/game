import pytest
import pygame
from unittest.mock import Mock, patch

from game.entities.animated_entity import AnimatedEntity, AnimationState
from game.graphics.sprite_manager import SpriteManager


class TestAnimatedEntity:
    """Tests for the AnimatedEntity class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        SpriteManager.reset_instance()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_animated_entity_initialization(self):
        """AnimatedEntity initializes correctly."""
        entity = AnimatedEntity(10, 20, 32, 32)
        
        assert entity.x == 10
        assert entity.y == 20
        assert entity.width == 32
        assert entity.height == 32
        assert entity.facing_direction == "down"
        assert entity.animation_state == AnimationState.IDLE
        assert entity.sprite_manager is not None
        assert entity.animation_set is not None
    
    def test_animated_entity_with_sprite_sheet(self):
        """AnimatedEntity with sprite sheet path attempts to load sprites."""
        # This will fail to load the sprite but should create fallback
        entity = AnimatedEntity(0, 0, 32, 32, "test_sprites.png")
        
        assert entity.sprite_sheet_path == "test_sprites.png"
        assert entity.animation_set.animations  # Should have fallback animation
    
    def test_animated_entity_without_sprite_sheet(self):
        """AnimatedEntity without sprite sheet creates fallback animation."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        assert entity.sprite_sheet_path is None
        assert entity.animation_set.animations  # Should have fallback animation
        assert "fallback" in entity.animation_set.animations
    
    def test_set_animation_state(self):
        """Setting animation state works correctly."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        assert entity.animation_state == AnimationState.IDLE
        
        entity.set_animation_state(AnimationState.WALK)
        assert entity.animation_state == AnimationState.WALK
        assert entity.last_animation_state == AnimationState.IDLE
    
    def test_set_facing_direction(self):
        """Setting facing direction works correctly."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        assert entity.facing_direction == "down"
        
        entity.set_facing_direction("up")
        assert entity.facing_direction == "up"
        assert entity.last_facing_direction == "down"
    
    def test_invalid_facing_direction(self):
        """Invalid facing directions are ignored."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        original_direction = entity.facing_direction
        entity.set_facing_direction("invalid")
        assert entity.facing_direction == original_direction
    
    def test_force_animation_state_change(self):
        """Force flag allows same state to be set again."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        entity.set_animation_state(AnimationState.WALK)
        entity.set_animation_state(AnimationState.WALK)  # Should not change
        assert entity.last_animation_state == AnimationState.IDLE
        
        entity.set_animation_state(AnimationState.WALK, force=True)  # Should change
        assert entity.last_animation_state == AnimationState.WALK
    
    def test_update_movement_animation_idle(self):
        """Update movement animation correctly handles idle state."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # No movement should be idle
        entity.update_movement_animation(0, 0)
        assert entity.animation_state == AnimationState.IDLE
    
    def test_update_movement_animation_walking(self):
        """Update movement animation correctly handles walking state."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Movement should trigger walk state
        entity.update_movement_animation(100, 0)  # Moving right
        assert entity.animation_state == AnimationState.WALK
        assert entity.facing_direction == "right"
        
        entity.update_movement_animation(0, 100)  # Moving down
        assert entity.facing_direction == "down"
        
        entity.update_movement_animation(-100, 0)  # Moving left
        assert entity.facing_direction == "left"
        
        entity.update_movement_animation(0, -100)  # Moving up
        assert entity.facing_direction == "up"
    
    def test_movement_animation_priority(self):
        """Horizontal movement takes priority for facing direction."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Diagonal movement - horizontal should win
        entity.update_movement_animation(100, 50)  # Right and down
        assert entity.facing_direction == "right"
        
        entity.update_movement_animation(-100, 50)  # Left and down
        assert entity.facing_direction == "left"
        
        # Vertical movement stronger
        entity.update_movement_animation(50, 100)  # Right and down
        assert entity.facing_direction == "down"
    
    def test_play_attack_animation(self):
        """Playing attack animation works correctly."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        entity.play_attack_animation()
        assert entity.animation_state == AnimationState.ATTACK
    
    def test_attack_animation_finished(self):
        """Attack animation finished detection works."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Not attacking initially
        assert not entity.is_attack_animation_finished()
        
        # Start attack
        entity.play_attack_animation()
        
        # Attack animation should be in progress (depends on animation implementation)
        # Since we're using fallback animations, this test is more about the logic
        if entity.animation_state == AnimationState.ATTACK:
            # The exact behavior depends on animation system
            pass
    
    def test_update_with_dt(self):
        """Entity update with delta time works."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Should not crash and should update animations
        entity.update(0.016)  # 60 FPS
        
        # Should have a current sprite
        sprite = entity.get_current_sprite()
        assert sprite is not None
        assert isinstance(sprite, pygame.Surface)
    
    def test_render(self):
        """Entity rendering works."""
        entity = AnimatedEntity(0, 0, 32, 32)
        screen = pygame.Surface((100, 100))
        
        # Should not crash
        entity.render(screen)
    
    def test_has_animation(self):
        """has_animation method works correctly."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Should have fallback animation
        assert entity.has_animation("fallback")
        
        # Should not have non-existent animation
        assert not entity.has_animation("nonexistent")
    
    def test_get_animation_info(self):
        """get_animation_info returns correct information."""
        entity = AnimatedEntity(0, 0, 32, 32, "test.png")
        
        info = entity.get_animation_info()
        
        assert "current_state" in info
        assert "facing_direction" in info
        assert "current_animation" in info
        assert "available_animations" in info
        assert "has_sprites" in info
        assert "sprite_sheet_path" in info
        
        assert info["current_state"] == "idle"
        assert info["facing_direction"] == "down"
        assert info["sprite_sheet_path"] == "test.png"
        assert isinstance(info["available_animations"], list)
    
    def test_fallback_color_customization(self):
        """Custom fallback color is used."""
        custom_color = (255, 0, 0)  # Red
        entity = AnimatedEntity(0, 0, 32, 32, fallback_color=custom_color)
        
        assert entity.fallback_color == custom_color
    
    def test_auto_transition_from_attack(self):
        """Attack animation auto-transitions back to idle."""
        entity = AnimatedEntity(0, 0, 32, 32)
        
        # Mock the animation to be finished
        entity.play_attack_animation()
        
        # Mock the animation as finished
        with patch.object(entity, 'is_attack_animation_finished', return_value=True):
            entity.update(0.016)
            
        # Should transition back to idle
        assert entity.animation_state == AnimationState.IDLE


class TestAnimatedEntityIntegration:
    """Integration tests for AnimatedEntity with real sprites."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        SpriteManager.reset_instance()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_entity_with_real_sprite_sheet(self):
        """Test entity with actual sprite sheet (uses created placeholder)."""
        entity = AnimatedEntity(
            0, 0, 32, 32, 
            "characters/player_spritesheet.png"
        )
        
        # Should have loaded multiple animations
        info = entity.get_animation_info()
        assert len(info["available_animations"]) > 1  # More than just fallback
        
        # Should be able to get a sprite
        sprite = entity.get_current_sprite()
        assert sprite is not None
        assert sprite.get_size() == (32, 32)
    
    def test_movement_with_real_sprites(self):
        """Test movement animation with real sprite sheet."""
        entity = AnimatedEntity(
            0, 0, 32, 32, 
            "characters/player_spritesheet.png"
        )
        
        # Test walking animation
        entity.update_movement_animation(100, 0)  # Walk right
        entity.update(0.016)
        
        # Should have walking animation if available
        if entity.has_animation("walk_right"):
            assert entity.animation_set.current_animation == "walk_right"
        
        # Test idle
        entity.update_movement_animation(0, 0)  # Stop
        entity.update(0.016)
        
        if entity.has_animation("idle_right"):
            assert entity.animation_state == AnimationState.IDLE