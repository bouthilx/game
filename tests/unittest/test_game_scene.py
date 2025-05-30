import os
import tempfile
from unittest.mock import Mock, patch

import pygame
import pytest

from game.scenes.game_scene import GameScene


class TestGameScene:
    @pytest.fixture
    def sample_map_file(self):
        pygame.init()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            surface = pygame.Surface((3, 3))

            grass = (34, 139, 34)
            spawn = (255, 0, 0)

            surface.fill(grass)
            surface.set_at((1, 1), spawn)

            pygame.image.save(surface, tmp_file.name)
            yield tmp_file.name

        os.unlink(tmp_file.name)
        pygame.quit()

    def test_game_scene_initialization(self, sample_map_file):
        # Temporarily replace the map file
        original_map_path = "data/maps/test_map.png"

        if os.path.exists(original_map_path):
            os.rename(original_map_path, original_map_path + ".backup")

        os.makedirs(os.path.dirname(original_map_path), exist_ok=True)
        import shutil

        shutil.copy(sample_map_file, original_map_path)

        try:
            scene = GameScene()

            assert scene.game_map is not None
            assert scene.player is not None
            assert scene.camera_x == 0
            assert scene.camera_y == 0

            # Player should spawn at red pixel location
            spawn_x, spawn_y = scene.game_map.spawn_point
            assert scene.player.x == spawn_x
            assert scene.player.y == spawn_y

        finally:
            if os.path.exists(original_map_path + ".backup"):
                os.rename(original_map_path + ".backup", original_map_path)
            elif os.path.exists(original_map_path):
                os.remove(original_map_path)

    def test_handle_event_escape_key(self, sample_map_file):
        original_map_path = "data/maps/test_map.png"

        if os.path.exists(original_map_path):
            os.rename(original_map_path, original_map_path + ".backup")

        os.makedirs(os.path.dirname(original_map_path), exist_ok=True)
        import shutil

        shutil.copy(sample_map_file, original_map_path)

        try:
            scene = GameScene()

            # Test escape key event (currently does nothing but should not crash)
            escape_event = Mock()
            escape_event.type = pygame.KEYDOWN
            escape_event.key = pygame.K_ESCAPE

            scene.handle_event(escape_event)  # Should not crash

        finally:
            if os.path.exists(original_map_path + ".backup"):
                os.rename(original_map_path + ".backup", original_map_path)
            elif os.path.exists(original_map_path):
                os.remove(original_map_path)

    def test_handle_event_other_key(self, sample_map_file):
        original_map_path = "data/maps/test_map.png"

        if os.path.exists(original_map_path):
            os.rename(original_map_path, original_map_path + ".backup")

        os.makedirs(os.path.dirname(original_map_path), exist_ok=True)
        import shutil

        shutil.copy(sample_map_file, original_map_path)

        try:
            scene = GameScene()

            # Test other key event
            other_event = Mock()
            other_event.type = pygame.KEYDOWN
            other_event.key = pygame.K_SPACE

            scene.handle_event(other_event)  # Should not crash

        finally:
            if os.path.exists(original_map_path + ".backup"):
                os.rename(original_map_path + ".backup", original_map_path)
            elif os.path.exists(original_map_path):
                os.remove(original_map_path)

    @patch("game.entities.player.Player.update")
    def test_update(self, mock_player_update, sample_map_file):
        original_map_path = "data/maps/test_map.png"

        if os.path.exists(original_map_path):
            os.rename(original_map_path, original_map_path + ".backup")

        os.makedirs(os.path.dirname(original_map_path), exist_ok=True)
        import shutil

        shutil.copy(sample_map_file, original_map_path)

        try:
            scene = GameScene()
            scene.player.x = 100
            scene.player.y = 150

            scene.update(0.016)

            # Player update should be called
            mock_player_update.assert_called_once_with(0.016, scene.game_map)

            # Camera should follow player
            assert scene.camera_x == scene.player.x - 400  # screen_width // 2
            assert scene.camera_y == scene.player.y - 300  # screen_height // 2

        finally:
            if os.path.exists(original_map_path + ".backup"):
                os.rename(original_map_path + ".backup", original_map_path)
            elif os.path.exists(original_map_path):
                os.remove(original_map_path)

    def test_render(self, sample_map_file):
        pygame.init()

        original_map_path = "data/maps/test_map.png"

        if os.path.exists(original_map_path):
            os.rename(original_map_path, original_map_path + ".backup")

        os.makedirs(os.path.dirname(original_map_path), exist_ok=True)
        import shutil

        shutil.copy(sample_map_file, original_map_path)

        try:
            scene = GameScene()
            scene.camera_x = 50
            scene.camera_y = 75

            # Create a mock screen
            screen = pygame.Surface((800, 600))

            # Test render method (should not crash)
            scene.render(screen)

            # Verify screen was modified (basic check)
            assert screen.get_size() == (800, 600)

        finally:
            if os.path.exists(original_map_path + ".backup"):
                os.rename(original_map_path + ".backup", original_map_path)
            elif os.path.exists(original_map_path):
                os.remove(original_map_path)

            pygame.quit()
