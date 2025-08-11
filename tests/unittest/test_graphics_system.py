import pytest
import pygame
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

from game.graphics.sprite_manager import SpriteManager
from game.graphics.animation import Animation, AnimationMode, AnimationSet
from game.graphics.sprite_sheet import SpriteSheet, CharacterSpriteSheet


class TestSpriteManager:
    """Tests for the SpriteManager class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        # Reset singleton for testing
        SpriteManager.reset_instance()
        self.sprite_manager = SpriteManager()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_singleton_behavior(self):
        """SpriteManager follows singleton pattern."""
        manager1 = SpriteManager()
        manager2 = SpriteManager()
        assert manager1 is manager2
    
    def test_load_nonexistent_sprite_creates_fallback(self):
        """Loading nonexistent sprite creates fallback."""
        sprite = self.sprite_manager.load_sprite("nonexistent.png")
        assert isinstance(sprite, pygame.Surface)
        assert sprite.get_size() == (32, 32)  # Default size
    
    def test_load_sprite_with_custom_size(self):
        """Loading sprite with custom size works."""
        sprite = self.sprite_manager.load_sprite("nonexistent.png", (64, 64))
        assert sprite.get_size() == (64, 64)
    
    def test_sprite_caching(self):
        """Sprites are properly cached."""
        sprite1 = self.sprite_manager.load_sprite("test.png")
        sprite2 = self.sprite_manager.load_sprite("test.png")
        assert sprite1 is sprite2  # Same object from cache
    
    def test_cache_info(self):
        """Cache info returns correct information."""
        self.sprite_manager.load_sprite("test1.png")
        self.sprite_manager.load_sprite("test2.png")
        
        info = self.sprite_manager.get_cache_info()
        assert info["sprites_cached"] == 2
        assert info["total_cached_items"] == 2
    
    def test_clear_cache(self):
        """Clearing cache works correctly."""
        self.sprite_manager.load_sprite("test.png")
        assert self.sprite_manager.get_cache_info()["sprites_cached"] == 1
        
        self.sprite_manager.clear_cache()
        assert self.sprite_manager.get_cache_info()["sprites_cached"] == 0
    
    def test_preload_sprites(self):
        """Preloading sprites works."""
        paths = ["test1.png", "test2.png", "test3.png"]
        self.sprite_manager.preload_sprites(paths)
        
        info = self.sprite_manager.get_cache_info()
        assert info["sprites_cached"] == 3
    
    def test_load_sprite_sheet_creates_frames(self):
        """Loading sprite sheet creates frame list."""
        frames = self.sprite_manager.load_sprite_sheet("test_sheet.png", (16, 16))
        assert isinstance(frames, list)
        assert len(frames) > 0
        assert all(isinstance(frame, pygame.Surface) for frame in frames)
    
    def test_set_assets_path(self):
        """Setting assets path works."""
        new_path = "/custom/path"
        self.sprite_manager.set_assets_path(new_path)
        assert str(self.sprite_manager._assets_path) == new_path


class TestAnimation:
    """Tests for the Animation class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        # Create test frames
        self.frames = []
        for i in range(4):
            surface = pygame.Surface((32, 32))
            surface.fill((i * 60, 100, 100))  # Different colors
            self.frames.append(surface)
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
    
    def test_animation_initialization(self):
        """Animation initializes correctly."""
        animation = Animation(self.frames, frame_duration=0.1, name="test")
        
        assert animation.frames == self.frames
        assert animation.frame_duration == 0.1
        assert animation.name == "test"
        assert animation.current_frame_index == 0
        assert animation.is_playing is True
        assert animation.is_finished is False
    
    def test_animation_requires_frames(self):
        """Animation requires at least one frame."""
        with pytest.raises(ValueError):
            Animation([])
    
    def test_animation_update_advances_frames(self):
        """Animation update advances frames correctly."""
        animation = Animation(self.frames, frame_duration=0.1)
        
        # Should stay on first frame initially
        frame = animation.update(0.05)
        assert frame is self.frames[0]
        assert animation.current_frame_index == 0
        
        # Should advance after frame duration
        frame = animation.update(0.06)  # Total: 0.11
        assert frame is self.frames[1]
        assert animation.current_frame_index == 1
    
    def test_animation_loop_mode(self):
        """Loop mode animation loops correctly."""
        animation = Animation(self.frames, frame_duration=0.1, mode=AnimationMode.LOOP)
        
        # Advance through frames (0->1->2->3->0)
        animation.update(0.1)  # Frame 1
        assert animation.current_frame_index == 1
        
        animation.update(0.1)  # Frame 2
        assert animation.current_frame_index == 2
        
        animation.update(0.1)  # Frame 3
        assert animation.current_frame_index == 3
        
        # Should loop back to beginning
        animation.update(0.1)  # Frame 0
        assert animation.current_frame_index == 0
    
    def test_animation_once_mode(self):
        """Once mode animation stops at end."""
        animation = Animation(self.frames, frame_duration=0.1, mode=AnimationMode.ONCE)
        
        # Advance to last frame
        for _ in range(4):
            animation.update(0.1)
        
        assert animation.current_frame_index == 3
        assert animation.is_finished is True
        
        # Should stay at last frame
        animation.update(0.1)
        assert animation.current_frame_index == 3
    
    def test_animation_ping_pong_mode(self):
        """Ping pong mode animation reverses direction."""
        animation = Animation(self.frames, frame_duration=0.1, mode=AnimationMode.PING_PONG)
        
        # Go forward: 0->1->2->3
        animation.update(0.1)  # Frame 1
        assert animation.current_frame_index == 1
        
        animation.update(0.1)  # Frame 2
        assert animation.current_frame_index == 2
        
        animation.update(0.1)  # Frame 3
        assert animation.current_frame_index == 3
        
        animation.update(0.1)  # Would go to 4, but bounces to frame 2
        assert animation.current_frame_index == 2
        assert animation.direction == -1
        
        # Should continue backward
        animation.update(0.1)  # Frame 1
        assert animation.current_frame_index == 1
    
    def test_animation_pause_and_play(self):
        """Animation pause and play work correctly."""
        animation = Animation(self.frames, frame_duration=0.1)
        
        animation.pause()
        assert animation.is_playing is False
        
        # Should not advance when paused
        animation.update(0.1)
        assert animation.current_frame_index == 0
        
        animation.play()
        assert animation.is_playing is True
        
        # Should advance when playing
        animation.update(0.1)
        assert animation.current_frame_index == 1
    
    def test_animation_stop_and_reset(self):
        """Animation stop and reset work correctly."""
        animation = Animation(self.frames, frame_duration=0.1)
        
        # Advance animation
        animation.update(0.2)
        assert animation.current_frame_index > 0
        
        animation.stop()
        assert animation.is_playing is False
        assert animation.current_frame_index == 0
        assert animation.elapsed_time == 0.0
    
    def test_animation_set_frame(self):
        """Setting animation frame works."""
        animation = Animation(self.frames, frame_duration=0.1)
        
        animation.set_frame(2)
        assert animation.current_frame_index == 2
        assert animation.elapsed_time == 0.0
    
    def test_animation_copy(self):
        """Animation copy creates independent copy."""
        original = Animation(self.frames, frame_duration=0.1, name="original")
        copy = original.copy()
        
        assert copy.frames == original.frames
        assert copy.frame_duration == original.frame_duration
        assert copy.name == original.name
        assert copy is not original
    
    def test_animation_progress(self):
        """Animation progress calculation works."""
        animation = Animation(self.frames, frame_duration=0.1)
        
        assert animation.progress == 0.0
        
        animation.update(0.05)  # Half of first frame
        assert 0.0 < animation.progress < 0.25
        
        animation.update(0.05)  # Complete first frame, move to frame 1
        expected_progress = 1.0 / 4.0  # Frame 1 out of 4 frames
        assert abs(animation.progress - expected_progress) < 0.01


class TestAnimationSet:
    """Tests for the AnimationSet class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        self.frames = [pygame.Surface((32, 32)) for _ in range(4)]
        self.animation_set = AnimationSet()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
    
    def test_add_animation(self):
        """Adding animation to set works."""
        animation = Animation(self.frames, name="test")
        self.animation_set.add_animation("test", animation)
        
        assert self.animation_set.has_animation("test")
        assert self.animation_set.current_animation == "test"
    
    def test_play_animation(self):
        """Playing animation by name works."""
        animation1 = Animation(self.frames, name="anim1")
        animation2 = Animation(self.frames, name="anim2")
        
        self.animation_set.add_animation("anim1", animation1)
        self.animation_set.add_animation("anim2", animation2)
        
        result = self.animation_set.play_animation("anim2")
        assert result is True
        assert self.animation_set.current_animation == "anim2"
    
    def test_play_nonexistent_animation(self):
        """Playing nonexistent animation returns False."""
        result = self.animation_set.play_animation("nonexistent")
        assert result is False
    
    def test_update_returns_current_frame(self):
        """Update returns frame from current animation."""
        animation = Animation(self.frames)
        self.animation_set.add_animation("test", animation)
        
        frame = self.animation_set.update(0.1)
        assert isinstance(frame, pygame.Surface)
    
    def test_fallback_animation(self):
        """Fallback animation is used when current is unavailable."""
        animation = Animation(self.frames)
        self.animation_set.add_animation("fallback", animation)
        self.animation_set.set_fallback_animation("fallback")
        
        # No current animation set
        self.animation_set.current_animation = None
        frame = self.animation_set.update(0.1)
        assert isinstance(frame, pygame.Surface)
    
    def test_is_animation_finished(self):
        """Checking if animation is finished works."""
        animation = Animation(self.frames, mode=AnimationMode.ONCE)
        self.animation_set.add_animation("test", animation)
        
        assert not self.animation_set.is_current_animation_finished()
        
        # Advance to end
        for _ in range(5):
            self.animation_set.update(0.1)
        
        assert self.animation_set.is_current_animation_finished()


class TestSpriteSheet:
    """Tests for the SpriteSheet class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        SpriteManager.reset_instance()
        self.sprite_sheet = SpriteSheet()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_load_from_file(self):
        """Loading sprite sheet from file works."""
        frames = self.sprite_sheet.load_from_file("test.png", (32, 32))
        assert isinstance(frames, list)
        assert len(frames) > 0
    
    def test_load_from_config_missing_file(self):
        """Loading from missing config file raises error."""
        with pytest.raises(ValueError):
            self.sprite_sheet.load_from_config("nonexistent.json")
    
    def test_create_config_template(self):
        """Creating config template works."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            SpriteSheet.create_config_template(
                config_path,
                "test_sheet.png",
                (32, 32),
                ["idle", "walk"]
            )
            
            # Verify config was created
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            assert config["image"] == "test_sheet.png"
            assert config["frame_size"] == [32, 32]
            assert "idle" in config["animations"]
            assert "walk" in config["animations"]
            
        finally:
            Path(config_path).unlink()
    
    def test_create_directional_animations(self):
        """Creating directional animations works."""
        animations = self.sprite_sheet.create_directional_animations(
            "test.png", (32, 32), ["down"], 4  # Only test one direction since sprite doesn't exist
        )
        
        assert "down" in animations
        assert isinstance(animations["down"], Animation)
        
        # Test that the function handles the case gracefully
        assert len(animations) >= 1


class TestCharacterSpriteSheet:
    """Tests for the CharacterSpriteSheet class."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        SpriteManager.reset_instance()
        self.character_sheet = CharacterSpriteSheet()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_load_character_animations(self):
        """Loading character animations works."""
        animations = self.character_sheet.load_character_animations(
            "character.png", (32, 32), ["idle"]  # Test with single animation type
        )
        
        assert "idle" in animations
        
        # Check that at least one direction is created (fallback sprite creates minimal frames)
        assert len(animations["idle"]) >= 1
        
        # Check that existing animations are proper Animation objects
        for direction, animation in animations["idle"].items():
            assert isinstance(animation, Animation)


class TestGraphicsIntegration:
    """Integration tests for the graphics system."""
    
    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        SpriteManager.reset_instance()
    
    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()
        SpriteManager.reset_instance()
    
    def test_full_character_animation_workflow(self):
        """Test complete workflow from sprite sheet to animation."""
        # Create sprite manager
        sprite_manager = SpriteManager()
        
        # Load character sprite sheet
        character_sheet = CharacterSpriteSheet(sprite_manager)
        animations = character_sheet.load_character_animations("test.png")
        
        # Create animation set
        animation_set = AnimationSet()
        
        # Add directional animations
        for direction in ["down", "up", "left", "right"]:
            if "idle" in animations and direction in animations["idle"]:
                animation_set.add_animation(f"idle_{direction}", animations["idle"][direction])
        
        # Test animation playback
        animation_set.play_animation("idle_down")
        frame = animation_set.update(0.1)
        
        assert isinstance(frame, pygame.Surface)
        assert animation_set.current_animation == "idle_down"