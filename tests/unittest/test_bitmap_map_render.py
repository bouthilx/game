import os
import tempfile

import pygame
import pytest

from game.world.bitmap_map import BitmapMap


class TestBitmapMapRender:
    @pytest.fixture
    def sample_map_file(self):
        pygame.init()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            surface = pygame.Surface((5, 5))

            grass = (34, 139, 34)
            wall = (165, 42, 42)
            water = (0, 0, 255)

            surface.fill(grass)
            # Add some walls and water
            surface.set_at((0, 0), wall)
            surface.set_at((4, 4), wall)
            surface.set_at((2, 2), water)

            pygame.image.save(surface, tmp_file.name)
            yield tmp_file.name

        os.unlink(tmp_file.name)
        pygame.quit()

    def test_render_full_map(self, sample_map_file):
        pygame.init()

        game_map = BitmapMap(sample_map_file, tile_size=32)
        screen = pygame.Surface((160, 160))  # 5x5 tiles * 32px

        # Render with camera at origin
        game_map.render(screen, 0, 0)

        # Check that screen was modified
        assert screen.get_size() == (160, 160)

        pygame.quit()

    def test_render_with_camera_offset(self, sample_map_file):
        pygame.init()

        game_map = BitmapMap(sample_map_file, tile_size=32)
        screen = pygame.Surface((160, 160))

        # Render with camera offset
        game_map.render(screen, 32, 32)

        # Should still render without errors
        assert screen.get_size() == (160, 160)

        pygame.quit()

    def test_render_partial_view(self, sample_map_file):
        pygame.init()

        game_map = BitmapMap(sample_map_file, tile_size=32)
        screen = pygame.Surface((64, 64))  # Smaller screen showing only 2x2 tiles

        # Render with camera showing only part of map
        game_map.render(screen, 64, 64)

        # Should render without errors
        assert screen.get_size() == (64, 64)

        pygame.quit()

    def test_render_camera_beyond_map(self, sample_map_file):
        pygame.init()

        game_map = BitmapMap(sample_map_file, tile_size=32)
        screen = pygame.Surface((160, 160))

        # Render with camera beyond map boundaries
        game_map.render(screen, 1000, 1000)

        # Should not crash
        assert screen.get_size() == (160, 160)

        pygame.quit()

    def test_render_negative_camera(self, sample_map_file):
        pygame.init()

        game_map = BitmapMap(sample_map_file, tile_size=32)
        screen = pygame.Surface((160, 160))

        # Render with negative camera position
        game_map.render(screen, -50, -50)

        # Should not crash
        assert screen.get_size() == (160, 160)

        pygame.quit()
