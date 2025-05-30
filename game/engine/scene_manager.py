from typing import List

import pygame

from game.engine.scene import Scene


class SceneManager:
    def __init__(self):
        self.scenes: List[Scene] = []

    def push_scene(self, scene: Scene):
        if self.scenes:
            self.scenes[-1].on_pause()
        self.scenes.append(scene)
        scene.on_enter()

    def pop_scene(self):
        if self.scenes:
            scene = self.scenes.pop()
            scene.on_exit()
            if self.scenes:
                self.scenes[-1].on_resume()

    def replace_scene(self, scene: Scene):
        if self.scenes:
            old_scene = self.scenes.pop()
            old_scene.on_exit()
        self.scenes.append(scene)
        scene.on_enter()

    def handle_event(self, event: pygame.event.Event):
        if self.scenes:
            self.scenes[-1].handle_event(event)

    def update(self, dt: float):
        if self.scenes:
            self.scenes[-1].update(dt)

    def render(self, screen: pygame.Surface):
        if self.scenes:
            self.scenes[-1].render(screen)
