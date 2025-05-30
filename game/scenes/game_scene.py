import pygame

from game.engine.scene import Scene
from game.entities.player import Player
from game.world.bitmap_map import BitmapMap


class GameScene(Scene):
    def __init__(self, map_path: str = "data/maps/object_test_map.png"):
        super().__init__()
        self.game_map = BitmapMap(map_path, tile_size=32)
        # Find a safe spawn position that avoids objects
        spawn_x, spawn_y = self.game_map.find_safe_spawn_position()
        self.player = Player(spawn_x, spawn_y)
        self.camera_x = 0
        self.camera_y = 0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass

    def update(self, dt: float):
        self.player.update(dt, self.game_map)

        screen_width = 800
        screen_height = 600
        self.camera_x = self.player.x - screen_width // 2
        self.camera_y = self.player.y - screen_height // 2

    def render(self, screen: pygame.Surface):
        # Render terrain layer first
        self.game_map.render_terrain(screen, self.camera_x, self.camera_y)

        # Render objects that should be behind the player (e.g., ground objects)
        # For now, let's render all objects behind the player
        self.game_map.render_objects(screen, self.camera_x, self.camera_y)

        # Render player on top of objects
        player_screen_x = self.player.x - self.camera_x
        player_screen_y = self.player.y - self.camera_y

        # Draw player directly at screen coordinates
        player_rect = pygame.Rect(int(player_screen_x), int(player_screen_y), self.player.width, self.player.height)
        pygame.draw.rect(screen, (0, 128, 255), player_rect)

        # Render UI elements on top
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        health_text = font.render(
            f"Health: {self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255),
        )

        screen.blit(level_text, (10, 10))
        screen.blit(health_text, (10, 50))
