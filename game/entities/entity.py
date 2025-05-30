from typing import Tuple

import pygame


class Entity:
    def __init__(self, x: float = 0, y: float = 0, width: int = 32, height: int = 32):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.speed = 100.0
        self.active = True

    @property
    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @position.setter
    def position(self, pos: Tuple[float, float]):
        self.x, self.y = pos

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt: float):
        if self.active:
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

    def render(self, screen: pygame.Surface):
        if self.active:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
