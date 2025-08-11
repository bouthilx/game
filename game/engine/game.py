import sys

import pygame

from game.engine.scene_manager import SceneManager
from game.scenes.game_scene import GameScene
from game.systems.sound_manager import get_sound_manager


class Game:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RPG Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        # Initialize sound manager
        self.sound_manager = get_sound_manager()

        self.scene_manager = SceneManager()
        self.scene_manager.push_scene(GameScene())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.scene_manager.handle_event(event)

    def update(self, dt: float):
        self.scene_manager.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.scene_manager.render(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update(dt)
            self.render()

        # Clean up sound manager
        self.sound_manager.cleanup()
        pygame.quit()
        sys.exit()
