"""
Controls Menu

Displays key bindings and controls for the game.
"""

import pygame
from typing import Optional, Callable
from .menu import Menu


class ControlsMenu(Menu):
    """Menu showing game controls and key bindings."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, "Controls")
        
        # Key bindings to display
        self.controls = [
            ("Movement", ""),
            ("  Move Up", "W / ↑"),
            ("  Move Down", "S / ↓"),
            ("  Move Left", "A / ←"),
            ("  Move Right", "D / →"),
            ("", ""),  # Spacer
            ("Combat", ""),
            ("  Attack", "SPACE"),
            ("  Switch Weapon", "1 / 2 / 3"),
            ("", ""),  # Spacer
            ("Interaction", ""),
            ("  Interact/Open Chest", "E"),
            ("  Open Inventory", "I"),
            ("  Open Equipment", "E (when not near objects)"),
            ("", ""),  # Spacer
            ("Menu", ""),
            ("  Open/Close Menu", "ESC"),
            ("  Navigate Menu", "↑↓ / W/S"),
            ("  Select", "Enter / Space"),
            ("", ""),  # Spacer
            ("Audio", ""),
            ("  Mute/Unmute", "M"),
            ("  Volume Up", "+ / ="),
            ("  Volume Down", "-"),
        ]
        
        # Scroll position for long lists
        self.scroll_position = 0
        self.max_visible_items = 12  # Adjust based on menu height
        
        # Callback for going back to main menu
        self.on_back: Optional[Callable] = None
    
    def navigate_up(self):
        """Scroll up through the controls list."""
        if self.scroll_position > 0:
            self.scroll_position -= 1
    
    def navigate_down(self):
        """Scroll down through the controls list."""
        max_scroll = max(0, len(self.controls) - self.max_visible_items)
        if self.scroll_position < max_scroll:
            self.scroll_position += 1
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events for the controls menu."""
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Go back to main menu
                if self.on_back:
                    self.on_back()
                return True
            
            elif event.key in [pygame.K_UP, pygame.K_w]:
                self.navigate_up()
                return True
            
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.navigate_down()
                return True
            
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                # Go back to main menu on Enter/Space
                if self.on_back:
                    self.on_back()
                return True
        
        return False
    
    def update(self, dt: float):
        """Update the controls menu."""
        pass  # No continuous updates needed
    
    def render(self, screen: pygame.Surface):
        """Render the controls menu."""
        if not self.visible:
            return
        
        # Draw background and border
        self.draw_background(screen)
        
        # Draw title
        title_y = self.draw_title(screen)
        
        # Calculate content area
        content_y = title_y + 20
        content_height = self.height - (content_y - self.y) - 60  # Leave space for instructions
        
        # Calculate line height and spacing
        line_height = 25
        start_y = content_y + 10
        
        # Get visible controls based on scroll position
        visible_controls = self.controls[self.scroll_position:self.scroll_position + self.max_visible_items]
        
        # Draw controls list
        for i, (action, key) in enumerate(visible_controls):
            y_pos = start_y + i * line_height
            
            # Skip if we're going outside the content area
            if y_pos + line_height > content_y + content_height:
                break
            
            if action == "":  # Spacer line
                continue
            
            # Choose color and font based on whether it's a category or item
            if key == "":  # Category headers (no key binding)
                color = self.selected_color  # Yellow for categories
                font = self.font
                action_text = action
            elif action.startswith("  "):  # Indented items
                color = self.text_color  # White for items
                font = self.small_font
                action_text = action
            else:
                color = self.text_color
                font = self.font
                action_text = action
            
            # Draw action name (left side)
            action_surface = font.render(action_text, True, color)
            screen.blit(action_surface, (self.x + 20, y_pos))
            
            # Draw key binding (right side)
            if key:
                key_color = (150, 150, 150)  # Gray for key names
                key_surface = font.render(key, True, key_color)
                key_x = self.x + self.width - key_surface.get_width() - 20
                screen.blit(key_surface, (key_x, y_pos))
        
        # Draw scroll indicator if needed
        if len(self.controls) > self.max_visible_items:
            # Show scroll position
            total_pages = (len(self.controls) + self.max_visible_items - 1) // self.max_visible_items
            current_page = (self.scroll_position // self.max_visible_items) + 1
            scroll_text = f"Page {current_page}/{total_pages}"
            scroll_surface = self.small_font.render(scroll_text, True, (150, 150, 150))
            scroll_x = self.x + self.width - scroll_surface.get_width() - 10
            scroll_y = content_y + content_height - 25
            screen.blit(scroll_surface, (scroll_x, scroll_y))
        
        # Draw instruction text at bottom
        instruction_text = "↑↓/WS: Scroll  Enter/Space/ESC: Back to Menu"
        instruction_surface = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_x = self.x + (self.width - instruction_surface.get_width()) // 2
        instruction_y = self.y + self.height - 30
        screen.blit(instruction_surface, (instruction_x, instruction_y))