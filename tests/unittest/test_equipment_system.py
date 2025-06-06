import pytest
import pygame
from unittest.mock import Mock

from game.equipment.weapon import Weapon, Sword, BasicSword, SteelSword, LegendarySword
from game.equipment.inventory import Inventory
from game.entities.player import Player


class TestWeaponSystem:
    """Tests du système d'armes."""

    def setup_method(self):
        """Setup pour chaque test."""
        self.basic_sword = BasicSword()
        self.steel_sword = SteelSword()
        self.legendary_sword = LegendarySword()

    def test_weapon_basic_attributes(self):
        """Les armes ont les attributs de base corrects."""
        assert self.basic_sword.name == "Épée de Base"
        assert self.basic_sword.damage == 20
        assert self.basic_sword.weapon_type == "sword"
        assert isinstance(self.basic_sword.description, str)

    def test_sword_progression(self):
        """Les épées ont une progression de dégâts logique."""
        assert self.basic_sword.damage < self.steel_sword.damage < self.legendary_sword.damage
        assert self.basic_sword.damage == 20
        assert self.steel_sword.damage == 35
        assert self.legendary_sword.damage == 50

    def test_weapon_stats(self):
        """Les stats des armes sont correctement retournées."""
        stats = self.basic_sword.get_stats()
        
        assert stats["name"] == "Épée de Base"
        assert stats["damage"] == 20
        assert stats["type"] == "sword"
        assert "description" in stats

    def test_weapon_str_representation(self):
        """La représentation string des armes est correcte."""
        assert str(self.basic_sword) == "Épée de Base (Dégâts: 20)"
        assert str(self.steel_sword) == "Épée d'Acier (Dégâts: 35)"


class TestInventorySystem:
    """Tests du système d'inventaire."""

    def setup_method(self):
        """Setup pour chaque test."""
        self.inventory = Inventory(max_size=5)  # Petit inventaire pour tester
        self.basic_sword = BasicSword()
        self.steel_sword = SteelSword()
        self.legendary_sword = LegendarySword()

    def test_inventory_initialization(self):
        """L'inventaire s'initialise correctement."""
        assert self.inventory.max_size == 5
        assert len(self.inventory.items) == 0
        assert self.inventory.equipped_weapon is None
        assert not self.inventory.is_full()

    def test_add_item_success(self):
        """Ajouter un objet à l'inventaire fonctionne."""
        result = self.inventory.add_item(self.basic_sword)
        
        assert result is True
        assert len(self.inventory.items) == 1
        assert self.basic_sword in self.inventory.items

    def test_add_item_inventory_full(self):
        """Ajouter un objet à un inventaire plein échoue."""
        # Remplir l'inventaire
        for i in range(5):
            sword = BasicSword()
            self.inventory.add_item(sword)
        
        assert self.inventory.is_full()
        
        # Tentative d'ajout d'un 6ème objet
        result = self.inventory.add_item(self.steel_sword)
        assert result is False
        assert len(self.inventory.items) == 5

    def test_remove_item(self):
        """Retirer un objet de l'inventaire fonctionne."""
        self.inventory.add_item(self.basic_sword)
        
        result = self.inventory.remove_item(self.basic_sword)
        assert result is True
        assert len(self.inventory.items) == 0
        assert self.basic_sword not in self.inventory.items

    def test_remove_item_not_present(self):
        """Retirer un objet absent de l'inventaire échoue."""
        result = self.inventory.remove_item(self.basic_sword)
        assert result is False

    def test_equip_weapon_success(self):
        """Équiper une arme fonctionne."""
        self.inventory.add_item(self.basic_sword)
        
        result = self.inventory.equip_weapon(self.basic_sword)
        assert result is True
        assert self.inventory.equipped_weapon == self.basic_sword

    def test_equip_weapon_not_in_inventory(self):
        """Équiper une arme qui n'est pas dans l'inventaire échoue."""
        result = self.inventory.equip_weapon(self.basic_sword)
        assert result is False
        assert self.inventory.equipped_weapon is None

    def test_equip_weapon_replaces_current(self):
        """Équiper une nouvelle arme remplace l'ancienne."""
        self.inventory.add_item(self.basic_sword)
        self.inventory.add_item(self.steel_sword)
        
        # Équiper la première arme
        self.inventory.equip_weapon(self.basic_sword)
        assert self.inventory.equipped_weapon == self.basic_sword
        
        # Équiper la deuxième arme
        self.inventory.equip_weapon(self.steel_sword)
        assert self.inventory.equipped_weapon == self.steel_sword

    def test_unequip_weapon(self):
        """Déséquiper une arme fonctionne."""
        self.inventory.add_item(self.basic_sword)
        self.inventory.equip_weapon(self.basic_sword)
        
        unequipped = self.inventory.unequip_weapon()
        assert unequipped == self.basic_sword
        assert self.inventory.equipped_weapon is None

    def test_unequip_weapon_none_equipped(self):
        """Déséquiper quand aucune arme n'est équipée retourne None."""
        unequipped = self.inventory.unequip_weapon()
        assert unequipped is None

    def test_get_weapons(self):
        """Récupérer toutes les armes fonctionne."""
        self.inventory.add_item(self.basic_sword)
        self.inventory.add_item(self.steel_sword)
        
        weapons = self.inventory.get_weapons()
        assert len(weapons) == 2
        assert self.basic_sword in weapons
        assert self.steel_sword in weapons

    def test_get_available_weapons(self):
        """Récupérer les armes non équipées fonctionne."""
        self.inventory.add_item(self.basic_sword)
        self.inventory.add_item(self.steel_sword)
        self.inventory.equip_weapon(self.basic_sword)
        
        available = self.inventory.get_available_weapons()
        assert len(available) == 1
        assert self.steel_sword in available
        assert self.basic_sword not in available

    def test_inventory_info(self):
        """Les informations d'inventaire sont correctes."""
        self.inventory.add_item(self.basic_sword)
        self.inventory.add_item(self.steel_sword)
        self.inventory.equip_weapon(self.basic_sword)
        
        info = self.inventory.get_inventory_info()
        
        assert info["items_count"] == 2
        assert info["max_size"] == 5
        assert info["equipped_weapon"] == "Épée de Base"
        assert len(info["weapons"]) == 2


class TestPlayerEquipmentIntegration:
    """Tests de l'intégration du système d'équipement avec le joueur."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.player = Player(100, 100)
    
    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_player_starts_with_basic_equipment(self):
        """Le joueur commence avec l'équipement de base."""
        equipped_weapon = self.player.inventory.get_equipped_weapon()
        
        assert equipped_weapon is not None
        assert equipped_weapon.name == "Épée de Base"
        assert len(self.player.inventory.get_weapons()) == 3  # Basic, Steel, Legendary

    def test_player_attack_damage_calculation(self):
        """Les dégâts d'attaque sont calculés correctement."""
        # Avec épée de base équipée
        damage = self.player.get_attack_damage()
        assert damage == 10 + 20  # base_damage + weapon_damage
        
        # Changer pour épée d'acier
        steel_sword = None
        for weapon in self.player.inventory.get_weapons():
            if weapon.name == "Épée d'Acier":
                steel_sword = weapon
                break
        
        assert steel_sword is not None
        self.player.equip_weapon(steel_sword)
        
        damage = self.player.get_attack_damage()
        assert damage == 10 + 35  # base_damage + steel_sword_damage

    def test_player_weapon_switching(self):
        """Le changement d'arme du joueur fonctionne."""
        # Vérifier arme initiale
        initial_weapon = self.player.inventory.get_equipped_weapon()
        assert initial_weapon.name == "Épée de Base"
        
        # Changer pour la deuxième arme
        self.player.handle_weapon_switch(pygame.K_2)
        current_weapon = self.player.inventory.get_equipped_weapon()
        assert current_weapon.name == "Épée d'Acier"
        
        # Changer pour la troisième arme
        self.player.handle_weapon_switch(pygame.K_3)
        current_weapon = self.player.inventory.get_equipped_weapon()
        assert current_weapon.name == "Épée Légendaire"
        
        # Retour à la première arme
        self.player.handle_weapon_switch(pygame.K_1)
        current_weapon = self.player.inventory.get_equipped_weapon()
        assert current_weapon.name == "Épée de Base"

    def test_player_add_to_inventory(self):
        """Ajouter des objets à l'inventaire du joueur fonctionne."""
        initial_count = self.player.inventory.get_item_count()
        
        new_sword = BasicSword()
        result = self.player.add_to_inventory(new_sword)
        
        assert result is True
        assert self.player.inventory.get_item_count() == initial_count + 1

    def test_player_damage_with_different_weapons(self):
        """Les dégâts changent selon l'arme équipée."""
        # Mock enemy pour tester les dégâts
        mock_enemy = Mock()
        mock_enemy.is_alive = True
        mock_enemy.take_damage.return_value = False  # Pas mort
        mock_enemy.check_collision_with_attack.return_value = True  # Touché
        
        enemies = [mock_enemy]
        
        # Équiper épée de base et attaquer
        self.player.handle_weapon_switch(pygame.K_1)
        self.player.start_attack(0)
        self.player.deal_damage_to_enemies(enemies)
        
        # Vérifier que l'ennemi a pris 30 dégâts (10 base + 20 épée)
        mock_enemy.take_damage.assert_called_with(30)
        
        # Reset mock et équiper épée légendaire
        mock_enemy.reset_mock()
        self.player.handle_weapon_switch(pygame.K_3)
        self.player.start_attack(1)  # Nouveau temps pour éviter cooldown
        self.player.deal_damage_to_enemies(enemies)
        
        # Vérifier que l'ennemi a pris 60 dégâts (10 base + 50 épée légendaire)
        mock_enemy.take_damage.assert_called_with(60)