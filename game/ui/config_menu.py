"""
Config Menu

Provides configuration options including separate volume controls for music and sound effects.
"""

import pygame
from typing import Optional, Callable
from .menu import Menu


class ConfigMenu(Menu):
    """Menu for game configuration options."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height, "Configuration")
        
        self.config_items = [
            "Music Volume",
            "Sound Effects Volume",
        ]
        
        self.selected_index = 0
        
        # Volume settings (0.0 to 1.0)
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
        # Callback for going back to main menu
        self.on_back: Optional[Callable] = None
        
        # Callback for volume changes
        self.on_music_volume_change: Optional[Callable[[float], None]] = None
        self.on_sfx_volume_change: Optional[Callable[[float], None]] = None
    
    def set_volumes(self, music_volume: float, sfx_volume: float):
        """Set the current volume levels."""
        self.music_volume = max(0.0, min(1.0, music_volume))
        self.sfx_volume = max(0.0, min(1.0, sfx_volume))
    
    def navigate_up(self):
        """Navigate to previous config item."""
        self.selected_index = (self.selected_index - 1) % len(self.config_items)
    
    def navigate_down(self):
        """Navigate to next config item."""
        self.selected_index = (self.selected_index + 1) % len(self.config_items)
    
    def adjust_value(self, increase: bool):
        """Adjust the value of the currently selected config item."""
        adjustment = 0.1 if increase else -0.1
        
        if self.selected_index == 0:  # Music Volume
            self.music_volume = max(0.0, min(1.0, self.music_volume + adjustment))
            if self.on_music_volume_change:
                self.on_music_volume_change(self.music_volume)
        
        elif self.selected_index == 1:  # Sound Effects Volume
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + adjustment))
            if self.on_sfx_volume_change:
                self.on_sfx_volume_change(self.sfx_volume)
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events for the config menu."""
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
            
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.adjust_value(False)  # Decrease
                return True
            
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.adjust_value(True)   # Increase
                return True
            
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                # Go back to main menu on Enter/Space
                if self.on_back:
                    self.on_back()
                return True
        
        return False
    
    def update(self, dt: float):
        """Update the config menu."""
        pass  # No continuous updates needed
    
    def draw_volume_bar(self, screen: pygame.Surface, x: int, y: int, width: int, volume: float):
        """Draw a volume bar with the current volume level."""
        bar_height = 20
        
        # Background bar
        bg_rect = pygame.Rect(x, y, width, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(screen, self.text_color, bg_rect, 2)
        
        # Volume fill
        fill_width = int(width * volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(x + 2, y + 2, fill_width - 4, bar_height - 4)
            # Color gradient from red (low) to green (high)
            if volume < 0.3:
                color = (255, int(255 * volume / 0.3), 0)  # Red to yellow
            elif volume < 0.7:
                color = (int(255 * (0.7 - volume) / 0.4), 255, 0)  # Yellow to green
            else:
                color = (0, 255, 0)  # Green
            
            pygame.draw.rect(screen, color, fill_rect)
        
        # Volume percentage text
        percentage = int(volume * 100)
        percent_text = f"{percentage}%"
        percent_surface = self.small_font.render(percent_text, True, self.text_color)
        percent_x = x + width + 10
        screen.blit(percent_surface, (percent_x, y + (bar_height - percent_surface.get_height()) // 2))
    
    def render(self, screen: pygame.Surface):
        """Render the config menu."""
        if not self.visible:
            return
        
        # Draw background and border
        self.draw_background(screen)
        
        # Draw title
        title_y = self.draw_title(screen)
        
        # Calculate content area
        content_y = title_y + 40
        content_height = self.height - (content_y - self.y) - 60  # Leave space for instructions
        
        # Calculate item spacing
        item_height = 80
        total_items_height = len(self.config_items) * item_height
        start_y = content_y + (content_height - total_items_height) // 2
        
        # Draw config items
        for i, item in enumerate(self.config_items):
            y_pos = start_y + i * item_height
            
            # Highlight selected item
            if i == self.selected_index:
                highlight_rect = pygame.Rect(
                    self.x + 10, y_pos - 10, 
                    self.width - 20, item_height - 10
                )
                pygame.draw.rect(screen, (40, 40, 40, 100), highlight_rect)
                pygame.draw.rect(screen, self.selected_color, highlight_rect, 2)
            
            # Draw item name
            text_surface = self.font.render(item, True, self.text_color)
            text_x = self.x + 30
            screen.blit(text_surface, (text_x, y_pos))
            
            # Draw volume control
            volume_bar_y = y_pos + 30
            volume_bar_width = 200
            volume_bar_x = self.x + 30
            
            if i == 0:  # Music Volume
                self.draw_volume_bar(screen, volume_bar_x, volume_bar_y, volume_bar_width, self.music_volume)
            elif i == 1:  # Sound Effects Volume
                self.draw_volume_bar(screen, volume_bar_x, volume_bar_y, volume_bar_width, self.sfx_volume)
        
        # Draw instruction text at bottom
        instruction_text = "↑↓/WS: Navigate  ←→/AD: Adjust  Enter/Space/ESC: Back"
        instruction_surface = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_x = self.x + (self.width - instruction_surface.get_width()) // 2
        instruction_y = self.y + self.height - 30
        screen.blit(instruction_surface, (instruction_x, instruction_y))