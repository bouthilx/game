import pygame

from game.entities.entity import Entity
from game.equipment.inventory import Inventory
from game.equipment.weapon import BasicSword, SteelSword, LegendarySword


class Player(Entity):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(x, y, 32, 32)
        self.speed = 150.0
        self.health = 100
        self.max_health = 100
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Equipment and inventory system
        self.inventory = Inventory(max_size=20)
        self.base_attack_damage = 10  # Dégâts de base sans arme
        
        # Ajouter différentes épées à l'inventaire pour tester
        basic_sword = BasicSword()
        steel_sword = SteelSword()
        legendary_sword = LegendarySword()
        
        self.inventory.add_item(basic_sword)
        self.inventory.add_item(steel_sword)
        self.inventory.add_item(legendary_sword)
        
        # Équiper l'épée de base au démarrage
        self.inventory.equip_weapon(basic_sword)
        
        # Combat system
        self.attack_range = 40
        self.attack_cooldown = 0.5  # seconds
        self.last_attack_time = -1  # Initialize to -1 so first attack works
        self.facing_direction = "down"  # down, up, left, right
        self.is_attacking = False
        self.attack_animation_time = 0.2  # seconds
        self.attack_start_time = 0
        self.enemies_hit_this_attack = set()  # Track enemies hit in current attack

    def handle_input(self, current_time: float, chest_manager=None):
        keys = pygame.key.get_pressed()

        # Movement input
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.facing_direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
            self.facing_direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
            self.facing_direction = "down"

        # Attack input
        if keys[pygame.K_SPACE] and self.can_attack(current_time):
            self.start_attack(current_time)
        
        # Chest interaction input
        if keys[pygame.K_e] and chest_manager:
            self.try_interact_with_chest(chest_manager)

    def handle_weapon_switch(self, key):
        """Gère le changement d'arme avec les touches numériques."""
        weapons = self.inventory.get_weapons()
        
        if key == pygame.K_1 and len(weapons) >= 1:
            self.inventory.equip_weapon(weapons[0])
        elif key == pygame.K_2 and len(weapons) >= 2:
            self.inventory.equip_weapon(weapons[1])
        elif key == pygame.K_3 and len(weapons) >= 3:
            self.inventory.equip_weapon(weapons[2])

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

    def get_attack_damage(self) -> int:
        """Calcule les dégâts d'attaque en fonction de l'arme équipée."""
        equipped_weapon = self.inventory.get_equipped_weapon()
        if equipped_weapon:
            return self.base_attack_damage + equipped_weapon.damage
        return self.base_attack_damage

    def equip_weapon(self, weapon):
        """Équipe une arme."""
        return self.inventory.equip_weapon(weapon)

    def add_to_inventory(self, item):
        """Ajoute un objet à l'inventaire."""
        return self.inventory.add_item(item)

    def try_interact_with_chest(self, chest_manager):
        """Essaie d'interagir avec un coffre proche."""
        # Utiliser le centre du joueur pour l'interaction
        player_center_x = self.x + self.width / 2
        player_center_y = self.y + self.height / 2
        
        chest = chest_manager.find_interactable_chest(player_center_x, player_center_y)
        if chest:
            loot_received = chest.open(self)
            if loot_received:
                # Retourner les objets reçus pour l'affichage dans l'UI
                return loot_received
        return []

    def can_attack(self, current_time: float) -> bool:
        return current_time - self.last_attack_time >= self.attack_cooldown

    def start_attack(self, current_time: float):
        self.is_attacking = True
        self.attack_start_time = current_time
        self.last_attack_time = current_time
        self.enemies_hit_this_attack.clear()  # Reset for new attack

    def get_attack_rect(self) -> pygame.Rect:
        """Get the rectangle representing the attack area."""
        if not self.is_attacking:
            return pygame.Rect(0, 0, 0, 0)
        
        attack_width = self.attack_range
        attack_height = self.attack_range
        
        if self.facing_direction == "right":
            attack_x = self.x + self.width
            attack_y = self.y + (self.height - attack_height) // 2
        elif self.facing_direction == "left":
            attack_x = self.x - attack_width
            attack_y = self.y + (self.height - attack_height) // 2
        elif self.facing_direction == "down":
            attack_x = self.x + (self.width - attack_width) // 2
            attack_y = self.y + self.height
        else:  # up
            attack_x = self.x + (self.width - attack_width) // 2
            attack_y = self.y - attack_height
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)

    def update_attack_state(self, current_time: float):
        """Update attack animation state."""
        if self.is_attacking:
            if current_time - self.attack_start_time >= self.attack_animation_time:
                self.is_attacking = False

    def check_attack_hits(self, enemies: list) -> list:
        """Vérifie si l'attaque touche des ennemis. Retourne la liste des ennemis touchés."""
        if not self.is_attacking:
            return []
        
        attack_rect = self.get_attack_rect()
        hit_enemies = []
        
        for enemy in enemies:
            if enemy.is_alive and enemy.check_collision_with_attack(attack_rect):
                hit_enemies.append(enemy)
        
        return hit_enemies

    def deal_damage_to_enemies(self, enemies: list) -> int:
        """Inflige des dégâts aux ennemis touchés. Retourne l'XP gagnée."""
        hit_enemies = self.check_attack_hits(enemies)
        total_xp = 0
        
        for enemy in hit_enemies:
            # Vérifier si cet ennemi a déjà été touché dans cette attaque
            if id(enemy) not in self.enemies_hit_this_attack:
                self.enemies_hit_this_attack.add(id(enemy))
                
                # Infliger dégâts basés sur l'arme équipée
                damage = self.get_attack_damage()
                enemy_died = enemy.take_damage(damage)
                
                # Si l'ennemi meurt, gagner de l'XP
                if enemy_died:
                    total_xp += enemy.experience_value
        
        return total_xp

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

    def update(self, dt: float, game_map=None, current_time: float = 0, chest_manager=None):
        self.handle_input(current_time, chest_manager)
        self.update_attack_state(current_time)

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
        # Render player
        pygame.draw.rect(screen, (0, 128, 255), self.rect)
        
        # Render attack area if attacking
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            pygame.draw.rect(screen, (255, 255, 0), attack_rect, 3)  # Yellow outline
