from typing import List, Optional

import pygame

from game.equipment.inventory import Inventory

from .menu import Menu


class InventoryMenu(Menu):
    """Menu for displaying and managing player inventory."""

    def __init__(self, x: int, y: int, width: int = 400, height: int = 500):
        super().__init__(x, y, width, height, "Inventory")
        self.inventory: Optional[Inventory] = None
        self.items_per_page = 15
        self.current_page = 0
        self.item_height = 25

    def set_inventory(self, inventory: Inventory):
        """Set the inventory to display."""
        self.inventory = inventory
        self.refresh_items()

    def refresh_items(self):
        """Refresh the items list from inventory."""
        if self.inventory:
            self.items = self.inventory.items.copy()
            # Reset selection if out of bounds
            if self.selected_index >= len(self.items):
                self.selected_index = max(0, len(self.items) - 1)
        else:
            self.items = []

    def on_show(self):
        """Refresh items when menu is shown."""
        self.refresh_items()

    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle inventory menu input."""
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.hide()
                return True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.navigate_up()
                return True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.navigate_down()
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.use_selected_item()
                return True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.previous_page()
                return True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.next_page()
                return True

        return False

    def use_selected_item(self):
        """Use/equip the selected item."""
        if self.items and 0 <= self.selected_index < len(self.items):
            item = self.items[self.selected_index]

            # If it's a weapon, try to equip it
            if hasattr(item, 'weapon_type') and self.inventory:
                if self.inventory.equip_weapon(item):
                    # Refresh to update equipped status
                    self.refresh_items()

    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.selected_index = 0

    def next_page(self):
        """Go to next page."""
        max_pages = (len(self.items) - 1) // self.items_per_page
        if self.current_page < max_pages:
            self.current_page += 1
            self.selected_index = 0

    def get_visible_items(self) -> List:
        """Get items for current page."""
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.items[start_idx:end_idx]

    def update(self, dt: float):
        """Update inventory menu."""
        pass  # No dynamic updates needed for now

    def render(self, screen: pygame.Surface):
        """Render the inventory menu."""
        if not self.visible:
            return

        # Draw background and title
        self.draw_background(screen)
        self.draw_title(screen)

        # Get content area
        content_x, content_y, content_width, content_height = self.get_content_area()

        # Draw inventory stats
        stats_y = content_y
        if self.inventory:
            stats_text = f"Items: {len(self.inventory.items)}/{self.inventory.max_size}"
            stats_surface = self.font.render(stats_text, True, self.text_color)
            screen.blit(stats_surface, (content_x, stats_y))

            # Draw gold (get from inventory's owner/player)
            gold_amount = "N/A"
            if hasattr(self.inventory, 'owner') and hasattr(self.inventory.owner, 'gold'):
                gold_amount = self.inventory.owner.gold
            gold_text = f"Gold: {gold_amount}"
            gold_surface = self.font.render(gold_text, True, (255, 215, 0))  # Gold color
            screen.blit(gold_surface, (content_x + content_width - gold_surface.get_width(), stats_y))

        # Draw page info
        max_pages = max(1, (len(self.items) + self.items_per_page - 1) // self.items_per_page)
        page_text = f"Page {self.current_page + 1}/{max_pages}"
        page_surface = self.small_font.render(page_text, True, self.text_color)
        screen.blit(page_surface, (content_x + (content_width - page_surface.get_width()) // 2, stats_y))

        # Draw items
        items_start_y = stats_y + 30
        visible_items = self.get_visible_items()

        for i, item in enumerate(visible_items):
            item_y = items_start_y + i * self.item_height

            # Determine if this item is selected
            global_index = self.current_page * self.items_per_page + i
            is_selected = global_index == self.selected_index

            # Draw selection highlight
            if is_selected:
                highlight_rect = pygame.Rect(content_x, item_y - 2, content_width, self.item_height)
                pygame.draw.rect(screen, (60, 60, 60), highlight_rect)
                pygame.draw.rect(screen, self.selected_color, highlight_rect, 2)

            # Draw item name
            item_name = str(item)
            text_color = self.selected_color if is_selected else self.text_color

            # Check if item is equipped
            is_equipped = (self.inventory and
                          hasattr(item, 'weapon_type') and
                          self.inventory.get_equipped_weapon() == item)

            if is_equipped:
                item_name += " [EQUIPPED]"
                text_color = (100, 255, 100)  # Green for equipped

            item_surface = self.font.render(item_name, True, text_color)
            screen.blit(item_surface, (content_x + 5, item_y))

            # Draw item stats if it's a weapon
            if hasattr(item, 'damage'):
                damage_text = f"Dmg: {item.damage}"
                damage_surface = self.small_font.render(damage_text, True, (200, 200, 200))
                screen.blit(damage_surface, (content_x + content_width - 80, item_y + 3))

        # Draw controls
        controls_y = content_y + content_height - 60
        controls = [
            "↑↓/WS: Navigate", "Enter/Space: Equip", "←→/AD: Page", "I/ESC: Close"
        ]

        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, (180, 180, 180))
            control_x = content_x + (i % 2) * (content_width // 2)
            control_y = controls_y + (i // 2) * 15
            screen.blit(control_surface, (control_x, control_y))
