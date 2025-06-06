import pytest
import pygame
from unittest.mock import Mock

from game.world.chest import ChestObject, ChestManager
from game.world.loot import LootGenerator, LootTable, LootItem, LootRarity, loot_generator
from game.entities.player import Player
from game.equipment.weapon import BasicSword, SteelSword, LegendarySword


class TestLootSystem:
    """Tests du système de butin."""

    def setup_method(self):
        """Setup pour chaque test."""
        self.loot_generator = LootGenerator()

    def test_loot_item_creation(self):
        """Test de création d'objets de butin."""
        # Gold item
        gold_item = LootItem("gold", 50, LootRarity.COMMON)
        assert gold_item.item_type == "gold"
        assert gold_item.item_data == 50
        assert gold_item.rarity == LootRarity.COMMON
        assert str(gold_item) == "50 pièces d'or"
        
        # Weapon item
        sword = BasicSword()
        weapon_item = LootItem("weapon", sword, LootRarity.UNCOMMON)
        assert weapon_item.item_type == "weapon"
        assert weapon_item.item_data == sword
        assert weapon_item.rarity == LootRarity.UNCOMMON
        assert str(weapon_item) == f"{sword.name} (uncommon)"

    def test_loot_table_creation(self):
        """Test de création d'une table de butin."""
        table = LootTable("test_table")
        assert table.name == "test_table"
        assert len(table.entries) == 0
        assert len(table.guaranteed_items) == 0
        
        # Ajouter des entrées
        table.add_entry("gold", 10, 50.0, LootRarity.COMMON)
        table.add_entry("weapon", BasicSword(), 25.0, LootRarity.COMMON)
        table.add_guaranteed_item("gold", 5, LootRarity.COMMON)
        
        assert len(table.entries) == 2
        assert len(table.guaranteed_items) == 1

    def test_loot_generation(self):
        """Test de génération de butin."""
        table = LootTable("test_table")
        table.add_entry("gold", 10, 50.0, LootRarity.COMMON)
        table.add_entry("gold", 25, 30.0, LootRarity.UNCOMMON)
        table.add_guaranteed_item("gold", 5, LootRarity.COMMON)
        
        # Générer du butin plusieurs fois
        for _ in range(10):
            loot = table.generate_loot(1)
            assert len(loot) == 2  # 1 garanti + 1 généré
            
            # Vérifier l'objet garanti
            guaranteed_found = any(item.item_data == 5 for item in loot)
            assert guaranteed_found

    def test_default_tables_exist(self):
        """Test que les tables par défaut existent."""
        assert self.loot_generator.get_table("basic_chest") is not None
        assert self.loot_generator.get_table("rare_chest") is not None
        assert self.loot_generator.get_table("legendary_chest") is not None
        assert self.loot_generator.get_table("enemy_basic") is not None

    def test_chest_loot_generation(self):
        """Test de génération de butin pour coffres."""
        # Coffre de base
        basic_loot = self.loot_generator.generate_chest_loot("basic_chest", 2)
        assert len(basic_loot) == 2
        
        # Coffre rare
        rare_loot = self.loot_generator.generate_chest_loot("rare_chest", 3)
        assert len(rare_loot) >= 3  # Au moins 3 (peut avoir des objets garantis)
        
        # Coffre légendaire
        legendary_loot = self.loot_generator.generate_chest_loot("legendary_chest", 4)
        assert len(legendary_loot) >= 4  # Au moins 4 (peut avoir des objets garantis)

    def test_invalid_table(self):
        """Test avec une table inexistante."""
        loot = self.loot_generator.generate_chest_loot("invalid_table", 2)
        assert loot == []


class TestChestSystem:
    """Tests du système de coffres."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.chest = ChestObject(100, 200, "basic_chest")
        self.player = Player(150, 220)

    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_chest_creation(self):
        """Test de création d'un coffre."""
        assert self.chest.name == "chest"
        assert self.chest.x == 100
        assert self.chest.y == 200
        assert self.chest.width == 32
        assert self.chest.height == 32
        assert self.chest.chest_type == "basic_chest"
        assert self.chest.is_opened is False
        assert self.chest.walkable is True
        assert len(self.chest.loot) > 0  # Du butin a été généré

    def test_chest_types(self):
        """Test des différents types de coffres."""
        basic_chest = ChestObject(0, 0, "basic_chest")
        rare_chest = ChestObject(0, 0, "rare_chest")
        legendary_chest = ChestObject(0, 0, "legendary_chest")
        
        assert basic_chest.chest_type == "basic_chest"
        assert rare_chest.chest_type == "rare_chest"
        assert legendary_chest.chest_type == "legendary_chest"
        
        # Les coffres plus rares devraient avoir plus de butin
        assert len(basic_chest.loot) <= len(rare_chest.loot)
        assert len(rare_chest.loot) <= len(legendary_chest.loot)

    def test_interaction_distance(self):
        """Test de la distance d'interaction."""
        # Joueur proche (centre du coffre : 116, 216)
        assert self.chest.can_interact_with(116, 216) is True  # Exactement au centre
        assert self.chest.can_interact_with(110, 210) is True  # Proche
        
        # Joueur dans le rayon d'interaction (40 pixels)
        assert self.chest.can_interact_with(156, 216) is True  # À droite, limite
        assert self.chest.can_interact_with(76, 216) is True   # À gauche, limite
        
        # Joueur hors du rayon d'interaction
        assert self.chest.can_interact_with(200, 200) is False  # Trop loin
        assert self.chest.can_interact_with(50, 50) is False    # Beaucoup trop loin

    def test_chest_opening(self):
        """Test d'ouverture de coffre."""
        initial_loot = list(self.chest.loot)  # Copie du butin initial
        initial_player_inventory_size = len(self.player.inventory.items)
        
        # Ouvrir le coffre
        received_loot = self.chest.open(self.player)
        
        # Le coffre devrait être ouvert
        assert self.chest.is_opened is True
        
        # Le joueur devrait avoir reçu du butin
        assert len(received_loot) > 0
        
        # L'inventaire du joueur devrait avoir changé
        assert len(self.player.inventory.items) >= initial_player_inventory_size

    def test_chest_already_opened(self):
        """Test qu'un coffre ouvert ne peut pas être rouvert."""
        # Ouvrir le coffre une première fois
        first_opening = self.chest.open(self.player)
        assert len(first_opening) > 0
        assert self.chest.is_opened is True
        
        # Essayer de l'ouvrir à nouveau
        second_opening = self.chest.open(self.player)
        assert len(second_opening) == 0  # Pas de butin
        
        # Le coffre reste ouvert
        assert self.chest.is_opened is True

    def test_interaction_prompt(self):
        """Test du message d'interaction."""
        # Coffre fermé
        assert self.chest.get_interaction_prompt() == "Appuyez sur E pour ouvrir"
        
        # Coffre ouvert
        self.chest.is_opened = True
        assert self.chest.get_interaction_prompt() == "Coffre vide"

    def test_can_interact_when_opened(self):
        """Test que l'interaction n'est pas possible avec un coffre ouvert."""
        # Fermer suffisamment près pour interagir
        assert self.chest.can_interact_with(116, 216) is True
        
        # Ouvrir le coffre
        self.chest.is_opened = True
        
        # L'interaction ne devrait plus être possible
        assert self.chest.can_interact_with(116, 216) is False

    def test_loot_summary(self):
        """Test du résumé de butin."""
        summary = self.chest.get_loot_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # Coffre vide
        empty_chest = ChestObject(0, 0, "basic_chest")
        empty_chest.loot = []
        assert empty_chest.get_loot_summary() == "Aucun butin"


class TestChestManager:
    """Tests du gestionnaire de coffres."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.chest_manager = ChestManager()
        self.player = Player(100, 100)

    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_chest_manager_creation(self):
        """Test de création du gestionnaire."""
        assert len(self.chest_manager.chests) == 0

    def test_add_chest(self):
        """Test d'ajout de coffre."""
        chest = ChestObject(50, 50, "basic_chest")
        self.chest_manager.add_chest(chest)
        
        assert len(self.chest_manager.chests) == 1
        assert self.chest_manager.chests[0] == chest

    def test_create_chest(self):
        """Test de création et ajout automatique."""
        chest = self.chest_manager.create_chest(75, 75, "rare_chest")
        
        assert len(self.chest_manager.chests) == 1
        assert chest.x == 75
        assert chest.y == 75
        assert chest.chest_type == "rare_chest"
        assert self.chest_manager.chests[0] == chest

    def test_find_interactable_chest(self):
        """Test de recherche de coffre interagissable."""
        # Créer des coffres à différentes distances
        close_chest = self.chest_manager.create_chest(110, 110, "basic_chest")  # Proche
        far_chest = self.chest_manager.create_chest(200, 200, "rare_chest")     # Loin
        
        # Joueur proche du premier coffre
        found_chest = self.chest_manager.find_interactable_chest(115, 115)
        assert found_chest == close_chest
        
        # Joueur loin de tous les coffres
        found_chest = self.chest_manager.find_interactable_chest(300, 300)
        assert found_chest is None

    def test_find_closest_interactable_chest(self):
        """Test de recherche du coffre le plus proche."""
        # Créer plusieurs coffres proches
        chest1 = self.chest_manager.create_chest(120, 120, "basic_chest")    # Plus proche
        chest2 = self.chest_manager.create_chest(130, 130, "rare_chest")     # Plus loin
        
        # Le gestionnaire devrait retourner le plus proche
        found_chest = self.chest_manager.find_interactable_chest(115, 115)
        assert found_chest == chest1

    def test_no_interaction_with_opened_chest(self):
        """Test qu'un coffre ouvert n'est pas trouvé comme interagissable."""
        chest = self.chest_manager.create_chest(110, 110, "basic_chest")
        
        # Avant ouverture
        found_chest = self.chest_manager.find_interactable_chest(115, 115)
        assert found_chest == chest
        
        # Après ouverture
        chest.is_opened = True
        found_chest = self.chest_manager.find_interactable_chest(115, 115)
        assert found_chest is None

    def test_get_stats(self):
        """Test des statistiques de coffres."""
        # Pas de coffres
        stats = self.chest_manager.get_stats()
        assert stats["total_chests"] == 0
        assert stats["opened_chests"] == 0
        assert stats["remaining_chests"] == 0
        
        # Ajouter des coffres
        chest1 = self.chest_manager.create_chest(50, 50, "basic_chest")
        chest2 = self.chest_manager.create_chest(100, 100, "rare_chest")
        
        stats = self.chest_manager.get_stats()
        assert stats["total_chests"] == 2
        assert stats["opened_chests"] == 0
        assert stats["remaining_chests"] == 2
        
        # Ouvrir un coffre
        chest1.is_opened = True
        
        stats = self.chest_manager.get_stats()
        assert stats["total_chests"] == 2
        assert stats["opened_chests"] == 1
        assert stats["remaining_chests"] == 1


class TestPlayerChestInteraction:
    """Tests d'interaction joueur-coffre."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.player = Player(100, 100)
        self.chest_manager = ChestManager()
        
        # Créer un coffre proche
        self.chest = self.chest_manager.create_chest(120, 120, "basic_chest")

    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_player_interact_with_chest(self):
        """Test d'interaction joueur-coffre."""
        initial_inventory_size = len(self.player.inventory.items)
        
        # Interagir avec le coffre
        loot_received = self.player.try_interact_with_chest(self.chest_manager)
        
        # Le joueur devrait avoir reçu du butin
        assert len(loot_received) > 0
        
        # L'inventaire devrait avoir changé
        assert len(self.player.inventory.items) >= initial_inventory_size
        
        # Le coffre devrait être ouvert
        assert self.chest.is_opened is True

    def test_player_interact_no_chest_nearby(self):
        """Test d'interaction sans coffre proche."""
        # Déplacer le joueur loin du coffre
        self.player.x = 300
        self.player.y = 300
        
        loot_received = self.player.try_interact_with_chest(self.chest_manager)
        
        # Aucun butin reçu
        assert len(loot_received) == 0
        
        # Le coffre reste fermé
        assert self.chest.is_opened is False

    def test_player_interact_opened_chest(self):
        """Test d'interaction avec un coffre déjà ouvert."""
        # Ouvrir le coffre d'abord
        self.chest.open(self.player)
        assert self.chest.is_opened is True
        
        # Essayer d'interagir à nouveau
        loot_received = self.player.try_interact_with_chest(self.chest_manager)
        
        # Aucun butin reçu
        assert len(loot_received) == 0

    def test_gold_conversion_to_experience(self):
        """Test que l'or est converti en XP (temporairement)."""
        initial_level = self.player.level
        initial_xp = self.player.experience
        
        # Placer le joueur plus près du coffre pour garantir l'interaction
        self.player.x = 120  # Centre du coffre : 136, 136
        self.player.y = 120
        
        # Forcer du butin avec de l'or (100 XP devrait faire level up)
        from game.world.loot import LootItem, LootRarity
        self.chest.loot = [LootItem("gold", 100, LootRarity.COMMON)]
        
        loot_received = self.player.try_interact_with_chest(self.chest_manager)
        
        # Le joueur devrait avoir reçu du butin
        assert len(loot_received) > 0
        assert any(item.item_type == "gold" for item in loot_received)
        
        # Le joueur devrait avoir levé up (100 XP avec 100 requis = level up)
        assert self.player.level > initial_level
        assert self.player.level == initial_level + 1
        
        # L'XP restante devrait être 0 (100 - 100 = 0)
        assert self.player.experience == 0