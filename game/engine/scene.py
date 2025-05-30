from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    def __init__(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_pause(self):
        pass

    def on_resume(self):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass
