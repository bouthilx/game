"""
Main Menu System

Provides the main game menu with options for Controls, Config, Save, and Resume.
"""

import pygame
from typing import Optional, Callable
from .menu import Menu


class MainMenu(Menu):
    """Main game menu with navigation to sub-menus."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, "Main Menu")
        
        self.menu_items = [
            "Resume",
            "Controls", 
            "Config",
            "Save",
        ]
        
        self.selected_index = 0
        
        # Callbacks for menu actions
        self.on_resume: Optional[Callable] = None
        self.on_controls: Optional[Callable] = None
        self.on_config: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
    
    def navigate_up(self):
        """Navigate to previous menu item."""
        self.selected_index = (self.selected_index - 1) % len(self.menu_items)
    
    def navigate_down(self):
        """Navigate to next menu item."""
        self.selected_index = (self.selected_index + 1) % len(self.menu_items)
    
    def select_current_item(self):
        """Execute the currently selected menu item."""
        selected_item = self.menu_items[self.selected_index]
        
        if selected_item == "Resume":
            if self.on_resume:
                self.on_resume()
        elif selected_item == "Controls":
            if self.on_controls:
                self.on_controls()
        elif selected_item == "Config":
            if self.on_config:
                self.on_config()
        elif selected_item == "Save":
            if self.on_save:
                self.on_save()
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events for the main menu."""
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC resumes the game (same as Resume)
                if self.on_resume:
                    self.on_resume()
                return True
            
            elif event.key in [pygame.K_UP, pygame.K_w]:
                self.navigate_up()
                return True
            
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.navigate_down()
                return True
            
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.select_current_item()
                return True
        
        return False
    
    def update(self, dt: float):
        """Update the main menu."""
        pass  # No continuous updates needed
    
    def render(self, screen: pygame.Surface):
        """Render the main menu."""
        if not self.visible:
            return
        
        # Draw background and border
        self.draw_background(screen)
        
        # Draw title
        title_y = self.draw_title(screen)
        
        # Calculate content area
        content_y = title_y + 20
        content_height = self.height - (content_y - self.y) - 20
        
        # Calculate item spacing
        item_height = 40
        total_items_height = len(self.menu_items) * item_height
        start_y = content_y + (content_height - total_items_height) // 2
        
        # Draw menu items
        for i, item in enumerate(self.menu_items):
            y_pos = start_y + i * item_height
            
            # Highlight selected item
            if i == self.selected_index:
                highlight_rect = pygame.Rect(
                    self.x + 10, y_pos - 5, 
                    self.width - 20, item_height - 10
                )
                pygame.draw.rect(screen, self.selected_color, highlight_rect)
                pygame.draw.rect(screen, self.text_color, highlight_rect, 2)
            
            # Draw menu item text
            text_surface = self.font.render(item, True, self.text_color)
            text_x = self.x + (self.width - text_surface.get_width()) // 2
            screen.blit(text_surface, (text_x, y_pos))
        
        # Draw instruction text at bottom
        instruction_text = "↑↓/WS: Navigate  Enter/Space: Select  ESC: Resume"
        instruction_surface = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_x = self.x + (self.width - instruction_surface.get_width()) // 2
        instruction_y = self.y + self.height - 30
        screen.blit(instruction_surface, (instruction_x, instruction_y))