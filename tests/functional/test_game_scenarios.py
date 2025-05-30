import os
import tempfile
from unittest.mock import patch

import pygame
import pytest

from game.entities.player import Player
from game.scenes.game_scene import GameScene
from game.world.bitmap_map import BitmapMap


class TestGameScenarios:
    @pytest.fixture
    def test_map_file(self):
        pygame.init()

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            surface = pygame.Surface((10, 10))

            grass = (34, 139, 34)
            wall = (165, 42, 42)
            spawn = (255, 0, 0)
            water = (0, 0, 255)
            chest = (255, 255, 0)

            # Fill with grass
            surface.fill(grass)

            # Create walls around border
            for x in range(10):
                surface.set_at((x, 0), wall)
                surface.set_at((x, 9), wall)
            for y in range(10):
                surface.set_at((0, y), wall)
                surface.set_at((9, y), wall)

            # Add water obstacle
            for x in range(3, 6):
                for y in range(3, 6):
                    surface.set_at((x, y), water)

            # Add spawn point and chest
            surface.set_at((1, 1), spawn)
            surface.set_at((7, 7), chest)

            pygame.image.save(surface, tmp_file.name)
            yield tmp_file.name

        os.unlink(tmp_file.name)
        pygame.quit()

    def test_player_spawn_at_correct_location(self, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)
        spawn_x, spawn_y = game_map.spawn_point

        # Spawn should be at tile (1,1) which is pixel (1*32+16, 1*32+16)
        assert spawn_x == 1 * 32 + 16
        assert spawn_y == 1 * 32 + 16

    def test_player_cannot_move_through_walls(self, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)
        player = Player(64, 64)  # Start at tile (2,2) - grass area

        # Try to move left into wall at (0, y)
        player.velocity_x = -100
        player.velocity_y = 0

        player.update(1.0, game_map)  # Large dt to ensure movement attempt

        # Should be blocked by wall
        assert player.x >= 32  # Should not go into wall tile

    @patch("game.entities.player.Player.handle_input")
    def test_player_cannot_move_through_water(self, mock_handle_input, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)
        player = Player(2 * 32 + 16, 2 * 32 + 16)  # Start at tile (2,2)

        # Try to move right into water area
        player.velocity_x = 100
        player.velocity_y = 100

        old_x, old_y = player.x, player.y
        player.update(1.0, game_map)

        # Should be blocked by water - player shouldn't move much
        assert abs(player.x - old_x) < 50  # Should be blocked before moving far
        assert abs(player.y - old_y) < 50

    @patch("game.entities.player.Player.handle_input")
    def test_player_can_move_on_grass(self, mock_handle_input, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)
        player = Player(2 * 32, 2 * 32)  # Start at grass tile

        # Move within grass area
        player.velocity_x = 32  # Move one tile right
        player.velocity_y = 0

        old_x = player.x
        player.update(1.0, game_map)

        # Should be able to move on grass
        assert player.x > old_x

    def test_player_movement_collision_boundary(self, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)

        # Position player right next to wall
        player = Player(32 + 16, 32 + 16)  # Center of tile (1,1) - spawn tile

        # Try to move up into wall
        player.velocity_x = 0
        player.velocity_y = -50

        player.update(1.0, game_map)

        # Should be blocked by top wall
        assert player.y >= 32  # Should not go above tile y=1

    def test_player_stats_and_leveling(self):
        player = Player()

        # Test initial stats
        assert player.level == 1
        assert player.health == 100
        assert player.max_health == 100
        assert player.experience == 0

        # Test experience gain and leveling
        player.gain_experience(100)
        assert player.level == 2
        assert player.max_health == 110
        assert player.health == 110  # Full heal on level up

        # Test damage and healing
        player.take_damage(50)
        assert player.health == 60

        player.heal(20)
        assert player.health == 80

    def test_map_tile_type_detection(self, test_map_file):
        game_map = BitmapMap(test_map_file, tile_size=32)

        # Test spawn tile
        spawn_tile = game_map.get_tile_at_grid(1, 1)
        assert spawn_tile.name == "spawn"
        assert spawn_tile.walkable is True

        # Test wall tile
        wall_tile = game_map.get_tile_at_grid(0, 0)
        assert wall_tile.name == "wall"
        assert wall_tile.walkable is False

        # Test water tile
        water_tile = game_map.get_tile_at_grid(4, 4)
        assert water_tile.name == "water"
        assert water_tile.walkable is False

        # Test chest tile
        chest_tile = game_map.get_tile_at_grid(7, 7)
        assert chest_tile.name == "chest"
        assert chest_tile.walkable is True

        # Test grass tile
        grass_tile = game_map.get_tile_at_grid(2, 2)
        assert grass_tile.name == "grass"
        assert grass_tile.walkable is True

    def test_game_scene_integration(self, test_map_file):
        # Test that GameScene properly integrates map and player
        # Use the test map file directly
        scene = GameScene(test_map_file)

        # Check that scene loaded map correctly
        assert scene.game_map is not None
        assert scene.game_map.width == 10  # test_map dimensions 
        assert scene.game_map.height == 10

        # Check that player spawned at correct location
        spawn_x, spawn_y = scene.game_map.spawn_point
        assert scene.player.x == spawn_x
        assert scene.player.y == spawn_y

        # Test scene update
        scene.update(0.016)

        # Camera should follow player
        assert scene.camera_x == scene.player.x - 400  # screen_width // 2
        assert scene.camera_y == scene.player.y - 300  # screen_height // 2

    def test_player_spawns_on_walkable_terrain(self, test_map_file):
        """Test that player always spawns on walkable terrain, not stuck on objects."""
        scene = GameScene(test_map_file)
        
        # Player should spawn on walkable terrain
        assert scene.game_map.is_walkable(scene.player.x, scene.player.y), \
            f"Player spawned at non-walkable position ({scene.player.x}, {scene.player.y})"
        
        # Player should be able to move in at least one direction
        can_move_up = scene.game_map.is_walkable(scene.player.x, scene.player.y - 32)
        can_move_down = scene.game_map.is_walkable(scene.player.x, scene.player.y + 32)
        can_move_left = scene.game_map.is_walkable(scene.player.x - 32, scene.player.y)
        can_move_right = scene.game_map.is_walkable(scene.player.x + 32, scene.player.y)
        
        assert any([can_move_up, can_move_down, can_move_left, can_move_right]), \
            "Player is completely surrounded by non-walkable terrain"
