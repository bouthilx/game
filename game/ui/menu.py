from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import pygame


class Menu(ABC):
    """Base class for all menu types."""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = "Menu"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.visible = False
        self.selected_index = 0
        self.items = []

        # Colors
        self.bg_color = (40, 40, 40, 200)  # Semi-transparent dark
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        self.selected_color = (255, 255, 100)
        self.title_color = (100, 200, 255)

        # Fonts (lazy initialization)
        self._title_font = None
        self._font = None
        self._small_font = None

    @property
    def title_font(self):
        """Lazy initialization of title font."""
        if self._title_font is None:
            self._title_font = pygame.font.Font(None, 32)
        return self._title_font

    @property
    def font(self):
        """Lazy initialization of font."""
        if self._font is None:
            self._font = pygame.font.Font(None, 24)
        return self._font

    @property
    def small_font(self):
        """Lazy initialization of small font."""
        if self._small_font is None:
            self._small_font = pygame.font.Font(None, 18)
        return self._small_font

    def show(self):
        """Show the menu."""
        self.visible = True
        self.on_show()

    def hide(self):
        """Hide the menu."""
        self.visible = False
        self.on_hide()

    def toggle(self):
        """Toggle menu visibility."""
        if self.visible:
            self.hide()
        else:
            self.show()

    def on_show(self):
        """Called when menu is shown. Override for custom behavior."""
        pass

    def on_hide(self):
        """Called when menu is hidden. Override for custom behavior."""
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events. Return True if event was consumed."""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Update menu state."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render the menu."""
        pass

    def navigate_up(self):
        """Move selection up."""
        if self.items:
            self.selected_index = (self.selected_index - 1) % len(self.items)

    def navigate_down(self):
        """Move selection down."""
        if self.items:
            self.selected_index = (self.selected_index + 1) % len(self.items)

    def draw_background(self, screen: pygame.Surface):
        """Draw menu background with border."""
        # Create surface with alpha for transparency
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        screen.blit(bg_surface, (self.x, self.y))

        # Draw border
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)

    def draw_title(self, screen: pygame.Surface):
        """Draw menu title."""
        title_text = self.title_font.render(self.title, True, self.title_color)
        title_x = self.x + (self.width - title_text.get_width()) // 2
        title_y = self.y + 10
        screen.blit(title_text, (title_x, title_y))

        # Draw underline
        line_start = (self.x + 20, title_y + title_text.get_height() + 5)
        line_end = (self.x + self.width - 20, title_y + title_text.get_height() + 5)
        pygame.draw.line(screen, self.title_color, line_start, line_end, 2)

    def get_content_area(self) -> Tuple[int, int, int, int]:
        """Get the content area (x, y, width, height) excluding title."""
        title_height = 50
        return (
            self.x + 10,
            self.y + title_height,
            self.width - 20,
            self.height - title_height - 10
        )


class MenuManager:
    """Manages multiple menus and their interactions."""

    def __init__(self):
        self.menus: List[Menu] = []
        self.active_menu: Optional[Menu] = None

    def add_menu(self, menu: Menu):
        """Add a menu to the manager."""
        self.menus.append(menu)

    def remove_menu(self, menu: Menu):
        """Remove a menu from the manager."""
        if menu in self.menus:
            if self.active_menu == menu:
                self.active_menu = None
            self.menus.remove(menu)

    def show_menu(self, menu: Menu):
        """Show a specific menu and hide others."""
        # Hide all other menus
        for m in self.menus:
            if m != menu:
                m.hide()

        menu.show()
        self.active_menu = menu

    def hide_all_menus(self):
        """Hide all menus."""
        for menu in self.menus:
            menu.hide()
        self.active_menu = None

    def get_visible_menus(self) -> List[Menu]:
        """Get all currently visible menus."""
        return [menu for menu in self.menus if menu.visible]

    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input for all visible menus. Return True if any menu consumed the event."""
        # Handle input for visible menus in reverse order (topmost first)
        for menu in reversed(self.get_visible_menus()):
            if menu.handle_input(event):
                return True
        return False

    def update(self, dt: float):
        """Update all visible menus."""
        for menu in self.get_visible_menus():
            menu.update(dt)

    def render(self, screen: pygame.Surface):
        """Render all visible menus."""
        for menu in self.get_visible_menus():
            menu.render(screen)

    def is_any_menu_visible(self) -> bool:
        """Check if any menu is currently visible."""
        return len(self.get_visible_menus()) > 0
