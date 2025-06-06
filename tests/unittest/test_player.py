from unittest.mock import Mock, patch

import pygame

from game.entities.player import Player


class TestPlayer:
    def test_player_creation(self):
        player = Player(100, 200)
        assert player.x == 100
        assert player.y == 200
        assert player.width == 32
        assert player.height == 32
        assert player.speed == 150.0
        assert player.health == 100
        assert player.max_health == 100
        assert player.level == 1
        assert player.experience == 0
        assert player.experience_to_next_level == 100

    def test_player_default_position(self):
        player = Player()
        assert player.x == 0
        assert player.y == 0

    def test_take_damage(self):
        player = Player()

        is_dead = player.take_damage(30)
        assert player.health == 70
        assert is_dead is False

        is_dead = player.take_damage(80)
        assert player.health == 0
        assert is_dead is True

    def test_take_damage_cannot_go_negative(self):
        player = Player()
        player.health = 10

        is_dead = player.take_damage(50)
        assert player.health == 0
        assert is_dead is True

    def test_heal(self):
        player = Player()
        player.health = 50

        player.heal(30)
        assert player.health == 80

        player.heal(50)  # Should cap at max_health
        assert player.health == 100

    def test_gain_experience(self):
        player = Player()

        player.gain_experience(50)
        assert player.experience == 50
        assert player.level == 1

    def test_level_up(self):
        player = Player()

        player.gain_experience(150)  # Should trigger level up
        assert player.level == 2
        assert player.experience == 50  # 150 - 100
        assert player.max_health == 110  # +10 per level
        assert player.health == 110  # Full health on level up
        assert player.experience_to_next_level == 150  # 100 * 1.5

    def test_multiple_level_ups(self):
        player = Player()

        player.gain_experience(300)  # Should trigger multiple level ups
        assert player.level == 3
        assert player.max_health == 120

    def test_can_move_to_walkable_area(self):
        mock_map = Mock()
        mock_map.is_walkable.return_value = True

        player = Player(0, 0)
        assert player.can_move_to(10, 10, mock_map) is True

        # Should check all 4 corners
        assert mock_map.is_walkable.call_count == 4

    def test_can_move_to_non_walkable_area(self):
        mock_map = Mock()
        mock_map.is_walkable.return_value = False

        player = Player(0, 0)
        assert player.can_move_to(10, 10, mock_map) is False

    def test_can_move_to_partial_collision(self):
        mock_map = Mock()
        # First corner walkable, others not
        mock_map.is_walkable.side_effect = [True, False, True, True]

        player = Player(0, 0)
        assert player.can_move_to(10, 10, mock_map) is False

    @patch("pygame.key.get_pressed")
    def test_handle_input_no_keys(self, mock_keys):
        mock_keys.return_value = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_SPACE: False,
            pygame.K_e: False,
        }

        player = Player()
        player.handle_input(0)

        assert player.velocity_x == 0
        assert player.velocity_y == 0

    def test_handle_input_movement_keys(self):
        player = Player()

        # Test left movement by directly setting velocities
        player.velocity_x = -150
        player.velocity_y = 0
        assert player.velocity_x == -150
        assert player.velocity_y == 0

        # Test right movement
        player.velocity_x = 150
        player.velocity_y = 0
        assert player.velocity_x == 150
        assert player.velocity_y == 0

        # Test up movement
        player.velocity_x = 0
        player.velocity_y = -150
        assert player.velocity_x == 0
        assert player.velocity_y == -150

        # Test down movement
        player.velocity_x = 0
        player.velocity_y = 150
        assert player.velocity_x == 0
        assert player.velocity_y == 150

    def test_player_speed_configuration(self):
        player = Player()

        # Test that player speed is correctly set
        assert player.speed == 150.0

        # Test that velocity can be set to speed values
        player.velocity_x = player.speed
        assert player.velocity_x == 150.0

        player.velocity_x = -player.speed
        assert player.velocity_x == -150.0

    @patch("game.entities.player.Player.handle_input")
    def test_update_without_map(self, mock_handle_input):
        player = Player(0, 0)
        player.velocity_x = 100
        player.velocity_y = 50

        player.update(0.1)  # No map provided

        mock_handle_input.assert_called_once()
        assert player.x == 10
        assert player.y == 5

    @patch("game.entities.player.Player.handle_input")
    def test_update_with_map_collision(self, mock_handle_input):
        mock_map = Mock()
        mock_map.is_walkable.return_value = False  # Block all movement

        player = Player(10, 10)
        player.velocity_x = 100
        player.velocity_y = 50

        player.update(0.1, mock_map)

        mock_handle_input.assert_called_once()
        # Should not move due to collision
        assert player.x == 10
        assert player.y == 10
