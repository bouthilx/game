from unittest.mock import Mock

import pygame

from game.entities.player import Player
from game.equipment.inventory import Inventory
from game.equipment.weapon import BasicSword, SteelSword
from game.ui.equipment_menu import EquipmentMenu
from game.ui.inventory_menu import InventoryMenu
from game.ui.menu import Menu, MenuManager


class TestMenuManager:
    """Tests for the MenuManager class."""

    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        self.menu_manager = MenuManager()

        # Create mock menus
        self.mock_menu1 = Mock(spec=Menu)
        self.mock_menu1.visible = False
        self.mock_menu2 = Mock(spec=Menu)
        self.mock_menu2.visible = False

    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()

    def test_menu_manager_initialization(self):
        """MenuManager initializes correctly."""
        assert len(self.menu_manager.menus) == 0
        assert self.menu_manager.active_menu is None

    def test_add_menu(self):
        """Adding menus to manager works."""
        self.menu_manager.add_menu(self.mock_menu1)
        assert len(self.menu_manager.menus) == 1
        assert self.mock_menu1 in self.menu_manager.menus

        self.menu_manager.add_menu(self.mock_menu2)
        assert len(self.menu_manager.menus) == 2

    def test_remove_menu(self):
        """Removing menus from manager works."""
        self.menu_manager.add_menu(self.mock_menu1)
        self.menu_manager.add_menu(self.mock_menu2)

        self.menu_manager.remove_menu(self.mock_menu1)
        assert len(self.menu_manager.menus) == 1
        assert self.mock_menu1 not in self.menu_manager.menus
        assert self.mock_menu2 in self.menu_manager.menus

    def test_show_menu(self):
        """Showing a menu works and hides others."""
        self.menu_manager.add_menu(self.mock_menu1)
        self.menu_manager.add_menu(self.mock_menu2)

        self.menu_manager.show_menu(self.mock_menu1)

        self.mock_menu1.show.assert_called_once()
        self.mock_menu2.hide.assert_called_once()
        assert self.menu_manager.active_menu == self.mock_menu1

    def test_hide_all_menus(self):
        """Hiding all menus works."""
        self.menu_manager.add_menu(self.mock_menu1)
        self.menu_manager.add_menu(self.mock_menu2)

        self.menu_manager.hide_all_menus()

        self.mock_menu1.hide.assert_called_once()
        self.mock_menu2.hide.assert_called_once()
        assert self.menu_manager.active_menu is None

    def test_get_visible_menus(self):
        """Getting visible menus works."""
        self.menu_manager.add_menu(self.mock_menu1)
        self.menu_manager.add_menu(self.mock_menu2)

        # No menus visible initially
        assert len(self.menu_manager.get_visible_menus()) == 0

        # Make one menu visible
        self.mock_menu1.visible = True
        visible_menus = self.menu_manager.get_visible_menus()
        assert len(visible_menus) == 1
        assert self.mock_menu1 in visible_menus

        # Make both visible
        self.mock_menu2.visible = True
        visible_menus = self.menu_manager.get_visible_menus()
        assert len(visible_menus) == 2

    def test_is_any_menu_visible(self):
        """Checking if any menu is visible works."""
        self.menu_manager.add_menu(self.mock_menu1)

        assert not self.menu_manager.is_any_menu_visible()

        self.mock_menu1.visible = True
        assert self.menu_manager.is_any_menu_visible()


class TestInventoryMenu:
    """Tests for the InventoryMenu class."""

    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        self.inventory_menu = InventoryMenu(100, 100, 400, 500)
        self.inventory = Inventory(max_size=10)

        # Add some test items
        self.basic_sword = BasicSword()
        self.steel_sword = SteelSword()
        self.inventory.add_item(self.basic_sword)
        self.inventory.add_item(self.steel_sword)

        self.inventory_menu.set_inventory(self.inventory)

    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()

    def test_inventory_menu_initialization(self):
        """InventoryMenu initializes correctly."""
        assert self.inventory_menu.x == 100
        assert self.inventory_menu.y == 100
        assert self.inventory_menu.width == 400
        assert self.inventory_menu.height == 500
        assert self.inventory_menu.title == "Inventory"
        assert not self.inventory_menu.visible

    def test_set_inventory(self):
        """Setting inventory updates menu items."""
        assert self.inventory_menu.inventory == self.inventory
        assert len(self.inventory_menu.items) == 2
        assert self.basic_sword in self.inventory_menu.items
        assert self.steel_sword in self.inventory_menu.items

    def test_refresh_items(self):
        """Refreshing items updates from inventory."""
        # Add new item to inventory
        new_sword = BasicSword()
        self.inventory.add_item(new_sword)

        # Items should not be updated yet
        assert len(self.inventory_menu.items) == 2

        # Refresh should update
        self.inventory_menu.refresh_items()
        assert len(self.inventory_menu.items) == 3
        assert new_sword in self.inventory_menu.items

    def test_navigation(self):
        """Menu navigation works correctly."""
        assert self.inventory_menu.selected_index == 0

        self.inventory_menu.navigate_down()
        assert self.inventory_menu.selected_index == 1

        self.inventory_menu.navigate_down()
        assert self.inventory_menu.selected_index == 0  # Wraps around

        self.inventory_menu.navigate_up()
        assert self.inventory_menu.selected_index == 1  # Wraps around

    def test_use_selected_item(self):
        """Using selected item equips weapons."""
        # Select first item (basic sword)
        self.inventory_menu.selected_index = 0

        # Use the item
        self.inventory_menu.use_selected_item()

        # Should be equipped
        assert self.inventory.get_equipped_weapon() == self.basic_sword

    def test_pagination(self):
        """Pagination works with many items."""
        # Create a larger inventory for testing pagination
        large_inventory = Inventory(max_size=25)

        # Add many items to test pagination
        for i in range(20):
            sword = BasicSword()
            large_inventory.add_item(sword)

        self.inventory_menu.set_inventory(large_inventory)

        # Should be on first page
        assert self.inventory_menu.current_page == 0
        visible_items = self.inventory_menu.get_visible_items()
        assert len(visible_items) == self.inventory_menu.items_per_page

        # Go to next page
        self.inventory_menu.next_page()
        assert self.inventory_menu.current_page == 1
        assert self.inventory_menu.selected_index == 0  # Reset selection

        # Go back
        self.inventory_menu.previous_page()
        assert self.inventory_menu.current_page == 0


class TestEquipmentMenu:
    """Tests for the EquipmentMenu class."""

    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        self.equipment_menu = EquipmentMenu(100, 100, 400, 350)
        self.player = Player(0, 0)
        self.equipment_menu.set_player(self.player)

    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()

    def test_equipment_menu_initialization(self):
        """EquipmentMenu initializes correctly."""
        assert self.equipment_menu.x == 100
        assert self.equipment_menu.y == 100
        assert self.equipment_menu.width == 400
        assert self.equipment_menu.height == 350
        assert self.equipment_menu.title == "Equipment & Stats"
        assert not self.equipment_menu.visible

    def test_set_player(self):
        """Setting player updates menu state."""
        assert self.equipment_menu.player == self.player
        assert self.equipment_menu.inventory == self.player.inventory

    def test_section_navigation(self):
        """Section navigation works correctly."""
        assert self.equipment_menu.selected_section == 0

        # Navigate right
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_RIGHT

        self.equipment_menu.visible = True
        result = self.equipment_menu.handle_input(event)

        assert result is True
        assert self.equipment_menu.selected_section == 1

        # Navigate left (wraps around)
        event.key = pygame.K_LEFT
        result = self.equipment_menu.handle_input(event)

        assert result is True
        assert self.equipment_menu.selected_section == 0

    def test_weapon_cycling(self):
        """Weapon cycling in equipment section works."""
        self.equipment_menu.visible = True
        self.equipment_menu.selected_section = 0  # Weapon section

        initial_weapon = self.player.inventory.get_equipped_weapon()

        # Navigate down to cycle weapon
        self.equipment_menu.navigate_down()
        new_weapon = self.player.inventory.get_equipped_weapon()

        # Should have changed to next weapon
        assert new_weapon != initial_weapon


class TestMenuIntegration:
    """Tests for menu system integration."""

    def setup_method(self):
        """Setup for each test."""
        pygame.init()
        self.player = Player(0, 0)
        self.menu_manager = MenuManager()

        # Create menus
        self.inventory_menu = InventoryMenu(100, 100)
        self.inventory_menu.set_inventory(self.player.inventory)

        self.equipment_menu = EquipmentMenu(100, 100)
        self.equipment_menu.set_player(self.player)

        # Add to manager
        self.menu_manager.add_menu(self.inventory_menu)
        self.menu_manager.add_menu(self.equipment_menu)

    def teardown_method(self):
        """Cleanup after each test."""
        pygame.quit()

    def test_menu_switching(self):
        """Switching between menus works correctly."""
        # Show inventory menu
        self.menu_manager.show_menu(self.inventory_menu)
        assert self.inventory_menu.visible
        assert not self.equipment_menu.visible

        # Switch to equipment menu
        self.menu_manager.show_menu(self.equipment_menu)
        assert not self.inventory_menu.visible
        assert self.equipment_menu.visible

    def test_input_handling_priority(self):
        """Input handling respects menu priority."""
        self.inventory_menu.visible = True

        # Create mock event
        event = Mock()
        event.type = pygame.KEYDOWN
        event.key = pygame.K_ESCAPE

        # Menu manager should handle input and return True
        result = self.menu_manager.handle_input(event)
        assert result is True
        assert not self.inventory_menu.visible  # Menu should be hidden

    def test_gold_display_integration(self):
        """Gold display integration works with player."""
        # Player should have starting gold
        assert self.player.gold == 100

        # Add some gold
        self.player.add_gold(50)
        assert self.player.gold == 150

        # Spend some gold
        result = self.player.spend_gold(25)
        assert result is True
        assert self.player.gold == 125

        # Try to spend more than available
        result = self.player.spend_gold(200)
        assert result is False
        assert self.player.gold == 125  # Should remain unchanged
