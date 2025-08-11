from typing import Optional

import pygame

from game.equipment.inventory import Inventory

from .menu import Menu


class EquipmentMenu(Menu):
    """Menu for equipment management and character stats."""

    def __init__(self, x: int, y: int, width: int = 400, height: int = 350):
        super().__init__(x, y, width, height, "Equipment & Stats")
        self.inventory: Optional[Inventory] = None
        self.player = None

        # Menu sections
        self.sections = ["weapon", "stats"]
        self.selected_section = 0

    def set_player(self, player):
        """Set the player to display stats for."""
        self.player = player
        if hasattr(player, 'inventory'):
            self.inventory = player.inventory

    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle equipment menu input."""
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                self.hide()
                return True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.navigate_up()
                return True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.navigate_down()
                return True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_section = (self.selected_section - 1) % len(self.sections)
                return True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_section = (self.selected_section + 1) % len(self.sections)
                return True
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                self.handle_weapon_switch(event.key)
                return True

        return False

    def handle_weapon_switch(self, key):
        """Handle weapon switching with number keys."""
        if self.player and hasattr(self.player, 'handle_weapon_switch'):
            self.player.handle_weapon_switch(key)

    def navigate_up(self):
        """Navigate within the selected section."""
        if self.sections[self.selected_section] == "weapon":
            # Cycle through available weapons
            if self.inventory:
                weapons = self.inventory.get_weapons()
                if weapons:
                    current_weapon = self.inventory.get_equipped_weapon()
                    if current_weapon in weapons:
                        current_idx = weapons.index(current_weapon)
                        new_idx = (current_idx - 1) % len(weapons)
                        self.inventory.equip_weapon(weapons[new_idx])

    def navigate_down(self):
        """Navigate within the selected section."""
        if self.sections[self.selected_section] == "weapon":
            # Cycle through available weapons
            if self.inventory:
                weapons = self.inventory.get_weapons()
                if weapons:
                    current_weapon = self.inventory.get_equipped_weapon()
                    if current_weapon in weapons:
                        current_idx = weapons.index(current_weapon)
                        new_idx = (current_idx + 1) % len(weapons)
                        self.inventory.equip_weapon(weapons[new_idx])

    def update(self, dt: float):
        """Update equipment menu."""
        pass  # No dynamic updates needed for now

    def render(self, screen: pygame.Surface):
        """Render the equipment menu."""
        if not self.visible:
            return

        # Draw background and title
        self.draw_background(screen)
        self.draw_title(screen)

        # Get content area
        content_x, content_y, content_width, content_height = self.get_content_area()

        # Split content into two columns
        left_width = content_width // 2 - 10
        right_width = content_width // 2 - 10
        left_x = content_x
        right_x = content_x + content_width // 2 + 10

        # Draw section headers
        weapon_color = self.selected_color if self.selected_section == 0 else self.text_color
        stats_color = self.selected_color if self.selected_section == 1 else self.text_color

        weapon_header = self.font.render("Equipment", True, weapon_color)
        stats_header = self.font.render("Character Stats", True, stats_color)

        screen.blit(weapon_header, (left_x, content_y))
        screen.blit(stats_header, (right_x, content_y))

        # Draw underlines for headers
        if self.selected_section == 0:
            pygame.draw.line(screen, weapon_color,
                           (left_x, content_y + 25),
                           (left_x + weapon_header.get_width(), content_y + 25), 2)
        if self.selected_section == 1:
            pygame.draw.line(screen, stats_color,
                           (right_x, content_y + 25),
                           (right_x + stats_header.get_width(), content_y + 25), 2)

        # Draw equipment section
        self.draw_equipment_section(screen, left_x, content_y + 40, left_width)

        # Draw stats section
        self.draw_stats_section(screen, right_x, content_y + 40, right_width)

        # Draw controls
        controls_y = content_y + content_height - 40
        controls = [
            "←→/AD: Switch Section", "↑↓/WS: Navigate", "1/2/3: Quick Equip", "E/ESC: Close"
        ]

        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, (180, 180, 180))
            control_x = content_x + (i % 2) * (content_width // 2)
            control_y = controls_y + (i // 2) * 15
            screen.blit(control_surface, (control_x, control_y))

    def draw_equipment_section(self, screen: pygame.Surface, x: int, y: int, width: int):
        """Draw the equipment section."""
        current_y = y

        if self.inventory:
            # Current weapon
            equipped_weapon = self.inventory.get_equipped_weapon()
            if equipped_weapon:
                weapon_text = f"Weapon: {equipped_weapon.name}"
                weapon_surface = self.font.render(weapon_text, True, (100, 255, 100))
                screen.blit(weapon_surface, (x, current_y))
                current_y += 25

                # Weapon stats
                damage_text = f"  Damage: {equipped_weapon.damage}"
                damage_surface = self.small_font.render(damage_text, True, self.text_color)
                screen.blit(damage_surface, (x, current_y))
                current_y += 20

                # Weapon type
                type_text = f"  Type: {equipped_weapon.weapon_type.title()}"
                type_surface = self.small_font.render(type_text, True, self.text_color)
                screen.blit(type_surface, (x, current_y))
                current_y += 30
            else:
                no_weapon_surface = self.font.render("No weapon equipped", True, (255, 100, 100))
                screen.blit(no_weapon_surface, (x, current_y))
                current_y += 30

            # Available weapons
            weapons = self.inventory.get_weapons()
            if weapons:
                available_text = "Available Weapons:"
                available_surface = self.font.render(available_text, True, self.text_color)
                screen.blit(available_surface, (x, current_y))
                current_y += 25

                for i, weapon in enumerate(weapons[:5]):  # Show first 5 weapons
                    is_equipped = weapon == equipped_weapon
                    prefix = "►" if is_equipped else f"{i+1}."
                    weapon_line = f"{prefix} {weapon.name} ({weapon.damage} dmg)"

                    color = (100, 255, 100) if is_equipped else self.text_color
                    weapon_line_surface = self.small_font.render(weapon_line, True, color)
                    screen.blit(weapon_line_surface, (x + 10, current_y))
                    current_y += 18

    def draw_stats_section(self, screen: pygame.Surface, x: int, y: int, width: int):
        """Draw the character stats section."""
        if not self.player:
            no_player_surface = self.font.render("No player data", True, (255, 100, 100))
            screen.blit(no_player_surface, (x, y))
            return

        current_y = y

        # Health
        health_text = f"Health: {self.player.health}/{self.player.max_health}"
        health_color = (255, 100, 100) if self.player.health < self.player.max_health // 2 else (100, 255, 100)
        health_surface = self.font.render(health_text, True, health_color)
        screen.blit(health_surface, (x, current_y))
        current_y += 25

        # Level and Experience
        level_text = f"Level: {self.player.level}"
        level_surface = self.font.render(level_text, True, self.text_color)
        screen.blit(level_surface, (x, current_y))
        current_y += 20

        exp_text = f"EXP: {self.player.experience}/{self.player.experience_to_next_level}"
        exp_surface = self.small_font.render(exp_text, True, self.text_color)
        screen.blit(exp_surface, (x, current_y))
        current_y += 30

        # Gold
        gold_text = f"Gold: {getattr(self.player, 'gold', 0)}"
        gold_surface = self.font.render(gold_text, True, (255, 215, 0))
        screen.blit(gold_surface, (x, current_y))
        current_y += 25

        # Combat stats
        combat_header = self.font.render("Combat Stats:", True, self.text_color)
        screen.blit(combat_header, (x, current_y))
        current_y += 25

        # Attack damage
        total_damage = self.player.get_attack_damage() if hasattr(self.player, 'get_attack_damage') else 0
        base_damage = getattr(self.player, 'base_attack_damage', 0)
        weapon_damage = total_damage - base_damage

        damage_text = f"  Attack: {total_damage} ({base_damage}+{weapon_damage})"
        damage_surface = self.small_font.render(damage_text, True, self.text_color)
        screen.blit(damage_surface, (x, current_y))
        current_y += 18

        # Attack speed
        cooldown = getattr(self.player, 'attack_cooldown', 0)
        speed_text = f"  Speed: {1/cooldown:.1f} atk/sec" if cooldown > 0 else "  Speed: N/A"
        speed_surface = self.small_font.render(speed_text, True, self.text_color)
        screen.blit(speed_surface, (x, current_y))
        current_y += 18
