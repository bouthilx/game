import pygame

from game.entities.entity import Entity


class Player(Entity):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(x, y, 32, 32)
        self.speed = 150.0
        self.health = 100
        self.max_health = 100
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed

    def take_damage(self, damage: int):
        self.health = max(0, self.health - damage)
        return self.health <= 0

    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)

    def gain_experience(self, amount: int):
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)

    def can_move_to(self, x: float, y: float, game_map) -> bool:
        margin = 2
        corners = [
            (x + margin, y + margin),
            (x + self.width - margin, y + margin),
            (x + margin, y + self.height - margin),
            (x + self.width - margin, y + self.height - margin),
        ]

        for corner_x, corner_y in corners:
            if not game_map.is_walkable(corner_x, corner_y):
                return False
        return True

    def update(self, dt: float, game_map=None):
        self.handle_input()

        if game_map:
            new_x = self.x + self.velocity_x * dt
            new_y = self.y + self.velocity_y * dt

            if self.can_move_to(new_x, self.y, game_map):
                self.x = new_x
            if self.can_move_to(self.x, new_y, game_map):
                self.y = new_y
        else:
            super().update(dt)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (0, 128, 255), self.rect)
