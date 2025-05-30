import os
import tempfile

import pygame
import pytest

from game.world.bitmap_map import BitmapMap


class TestBitmapMap:
    @pytest.fixture
    def sample_map_file(self):
        pygame.init()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            surface = pygame.Surface((5, 5))

            grass = (34, 139, 34)
            wall = (165, 42, 42)
            spawn = (255, 0, 0)
            water = (0, 0, 255)

            surface.fill(grass)
            surface.set_at((0, 0), wall)
            surface.set_at((4, 4), wall)
            surface.set_at((1, 1), spawn)
            surface.set_at((2, 2), water)

            pygame.image.save(surface, tmp_file.name)
            yield tmp_file.name

        os.unlink(tmp_file.name)
        pygame.quit()

    def test_map_loading(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)
        assert game_map.width == 5
        assert game_map.height == 5
        assert game_map.tile_size == 32

    def test_spawn_point_detection(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)
        spawn_x, spawn_y = game_map.spawn_point
        assert spawn_x == 1 * 32 + 16  # tile 1 center
        assert spawn_y == 1 * 32 + 16  # tile 1 center

    def test_get_tile_at_grid(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)

        wall_tile = game_map.get_tile_at_grid(0, 0)
        assert wall_tile.name == "wall"
        assert not wall_tile.walkable

        spawn_tile = game_map.get_tile_at_grid(1, 1)
        assert spawn_tile.name == "spawn"
        assert spawn_tile.walkable

        water_tile = game_map.get_tile_at_grid(2, 2)
        assert water_tile.name == "water"
        assert not water_tile.walkable

    def test_get_tile_at_pixel(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)

        wall_tile = game_map.get_tile_at_pixel(15, 15)  # Inside tile (0,0)
        assert wall_tile.name == "wall"

        spawn_tile = game_map.get_tile_at_pixel(47, 47)  # Inside tile (1,1)
        assert spawn_tile.name == "spawn"

    def test_is_walkable(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)

        assert not game_map.is_walkable(15, 15)  # Wall
        assert game_map.is_walkable(47, 47)  # Spawn point
        assert not game_map.is_walkable(79, 79)  # Water

    def test_out_of_bounds_returns_void(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)

        void_tile = game_map.get_tile_at_grid(-1, -1)
        assert void_tile.name == "void"
        assert not void_tile.walkable

        void_tile = game_map.get_tile_at_grid(10, 10)
        assert void_tile.name == "void"
        assert not void_tile.walkable

    def test_world_size(self, sample_map_file):
        game_map = BitmapMap(sample_map_file, tile_size=32)
        width, height = game_map.get_world_size()
        assert width == 5 * 32
        assert height == 5 * 32
