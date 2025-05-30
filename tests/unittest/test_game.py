from unittest.mock import Mock, patch

import pygame

from game.engine.game import Game


class TestGame:
    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_game_initialization(
        self, mock_clock, mock_caption, mock_set_mode, mock_init
    ):
        mock_screen = Mock()
        mock_set_mode.return_value = mock_screen
        mock_clock_instance = Mock()
        mock_clock.return_value = mock_clock_instance

        game = Game(800, 600)

        mock_init.assert_called_once()
        mock_set_mode.assert_called_once_with((800, 600))
        mock_caption.assert_called_once_with("RPG Game")

        assert game.width == 800
        assert game.height == 600
        assert game.screen == mock_screen
        assert game.running is True
        assert game.fps == 60
        assert game.clock == mock_clock_instance

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_game_default_size(
        self, mock_clock, mock_caption, mock_set_mode, mock_init
    ):
        game = Game()

        mock_set_mode.assert_called_once_with((800, 600))
        assert game.width == 800
        assert game.height == 600

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.event.get")
    def test_handle_events_quit(
        self, mock_get_events, mock_clock, mock_caption, mock_set_mode, mock_init
    ):
        quit_event = Mock()
        quit_event.type = pygame.QUIT
        mock_get_events.return_value = [quit_event]

        game = Game()
        game.handle_events()

        assert game.running is False

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.event.get")
    def test_handle_events_other(
        self, mock_get_events, mock_clock, mock_caption, mock_set_mode, mock_init
    ):
        other_event = Mock()
        other_event.type = pygame.KEYDOWN
        mock_get_events.return_value = [other_event]

        game = Game()
        game.scene_manager = Mock()
        game.handle_events()

        game.scene_manager.handle_event.assert_called_once_with(other_event)
        assert game.running is True

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    def test_update(self, mock_clock, mock_caption, mock_set_mode, mock_init):
        game = Game()
        game.scene_manager = Mock()

        game.update(0.016)

        game.scene_manager.update.assert_called_once_with(0.016)

    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("pygame.display.flip")
    def test_render(
        self, mock_flip, mock_clock, mock_caption, mock_set_mode, mock_init
    ):
        mock_screen = Mock()
        mock_set_mode.return_value = mock_screen

        game = Game()
        game.scene_manager = Mock()

        game.render()

        mock_screen.fill.assert_called_once_with((0, 0, 0))
        game.scene_manager.render.assert_called_once_with(mock_screen)
        mock_flip.assert_called_once()
