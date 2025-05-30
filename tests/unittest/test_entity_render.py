import pygame

from game.entities.entity import Entity
from game.entities.player import Player


class TestEntityRender:
    def test_entity_render_active(self):
        pygame.init()

        entity = Entity(10, 20, 32, 32)
        entity.active = True
        screen = pygame.Surface((100, 100))

        # Should render without errors
        entity.render(screen)

        # Verify screen was modified
        assert screen.get_size() == (100, 100)

        pygame.quit()

    def test_entity_render_inactive(self):
        pygame.init()

        entity = Entity(10, 20, 32, 32)
        entity.active = False
        screen = pygame.Surface((100, 100))

        # Should not render when inactive
        entity.render(screen)

        # Should not crash
        assert screen.get_size() == (100, 100)

        pygame.quit()

    def test_player_render(self):
        pygame.init()

        player = Player(50, 60)
        screen = pygame.Surface((200, 200))

        # Should render player as blue rectangle
        player.render(screen)

        # Verify screen was modified
        assert screen.get_size() == (200, 200)

        pygame.quit()
