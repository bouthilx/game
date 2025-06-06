"""
Système de butin pour les coffres et ennemis.
"""
import random
from typing import List, Dict, Any, Optional
from enum import Enum

from game.equipment.weapon import BasicSword, SteelSword, LegendarySword


class LootRarity(Enum):
    """Rareté des objets de butin."""
    COMMON = "common"
    UNCOMMON = "uncommon" 
    RARE = "rare"
    LEGENDARY = "legendary"


class LootItem:
    """Représente un objet de butin."""
    
    def __init__(self, item_type: str, item_data: Any, rarity: LootRarity = LootRarity.COMMON):
        self.item_type = item_type  # "weapon", "gold", "consumable", etc.
        self.item_data = item_data  # L'objet réel (arme, montant d'or, etc.)
        self.rarity = rarity
    
    def __str__(self) -> str:
        if self.item_type == "gold":
            return f"{self.item_data} pièces d'or"
        elif self.item_type == "weapon":
            return f"{self.item_data.name} ({self.rarity.value})"
        else:
            return f"{self.item_type}: {self.item_data}"


class LootEntry:
    """Entrée dans une table de butin."""
    
    def __init__(self, item_type: str, item_data: Any, weight: float, rarity: LootRarity = LootRarity.COMMON):
        self.item_type = item_type
        self.item_data = item_data
        self.weight = weight  # Probabilité relative
        self.rarity = rarity


class LootTable:
    """Table de butin pour générer des objets aléatoires."""
    
    def __init__(self, name: str):
        self.name = name
        self.entries: List[LootEntry] = []
        self.guaranteed_items: List[LootItem] = []  # Objets toujours présents
    
    def add_entry(self, item_type: str, item_data: Any, weight: float, rarity: LootRarity = LootRarity.COMMON):
        """Ajoute une entrée à la table de butin."""
        self.entries.append(LootEntry(item_type, item_data, weight, rarity))
    
    def add_guaranteed_item(self, item_type: str, item_data: Any, rarity: LootRarity = LootRarity.COMMON):
        """Ajoute un objet garanti à la table."""
        self.guaranteed_items.append(LootItem(item_type, item_data, rarity))
    
    def generate_loot(self, num_rolls: int = 1) -> List[LootItem]:
        """Génère du butin selon la table."""
        loot = []
        
        # Ajouter les objets garantis
        loot.extend(self.guaranteed_items.copy())
        
        # Générer des objets aléatoires
        for _ in range(num_rolls):
            if not self.entries:
                continue
                
            # Calculer le poids total
            total_weight = sum(entry.weight for entry in self.entries)
            
            # Sélectionner un objet au hasard
            roll = random.uniform(0, total_weight)
            current_weight = 0
            
            for entry in self.entries:
                current_weight += entry.weight
                if roll <= current_weight:
                    loot.append(LootItem(entry.item_type, entry.item_data, entry.rarity))
                    break
        
        return loot


class LootGenerator:
    """Générateur principal de butin pour différents contextes."""
    
    def __init__(self):
        self.tables: Dict[str, LootTable] = {}
        self._create_default_tables()
    
    def _create_default_tables(self):
        """Crée les tables de butin par défaut."""
        
        # Table pour coffres de base
        basic_chest = LootTable("basic_chest")
        basic_chest.add_entry("gold", 10, 30.0, LootRarity.COMMON)
        basic_chest.add_entry("gold", 25, 20.0, LootRarity.COMMON)
        basic_chest.add_entry("gold", 50, 10.0, LootRarity.UNCOMMON)
        basic_chest.add_entry("weapon", BasicSword(), 15.0, LootRarity.COMMON)
        basic_chest.add_entry("weapon", SteelSword(), 5.0, LootRarity.UNCOMMON)
        self.tables["basic_chest"] = basic_chest
        
        # Table pour coffres rares
        rare_chest = LootTable("rare_chest")
        rare_chest.add_entry("gold", 50, 25.0, LootRarity.UNCOMMON)
        rare_chest.add_entry("gold", 100, 15.0, LootRarity.RARE)
        rare_chest.add_entry("weapon", SteelSword(), 20.0, LootRarity.UNCOMMON)
        rare_chest.add_entry("weapon", LegendarySword(), 10.0, LootRarity.RARE)
        # Objet garanti dans les coffres rares
        rare_chest.add_guaranteed_item("gold", 25, LootRarity.COMMON)
        self.tables["rare_chest"] = rare_chest
        
        # Table pour coffres légendaires
        legendary_chest = LootTable("legendary_chest")
        legendary_chest.add_entry("gold", 100, 20.0, LootRarity.RARE)
        legendary_chest.add_entry("gold", 250, 15.0, LootRarity.LEGENDARY)
        legendary_chest.add_entry("weapon", LegendarySword(), 30.0, LootRarity.LEGENDARY)
        # Objets garantis dans les coffres légendaires
        legendary_chest.add_guaranteed_item("gold", 50, LootRarity.UNCOMMON)
        legendary_chest.add_guaranteed_item("weapon", SteelSword(), LootRarity.UNCOMMON)
        self.tables["legendary_chest"] = legendary_chest
        
        # Table pour ennemis (pour plus tard)
        enemy_loot = LootTable("enemy_basic")
        enemy_loot.add_entry("gold", 5, 40.0, LootRarity.COMMON)
        enemy_loot.add_entry("gold", 10, 20.0, LootRarity.COMMON)
        enemy_loot.add_entry("weapon", BasicSword(), 5.0, LootRarity.COMMON)
        self.tables["enemy_basic"] = enemy_loot
    
    def get_table(self, table_name: str) -> Optional[LootTable]:
        """Récupère une table de butin par nom."""
        return self.tables.get(table_name)
    
    def generate_chest_loot(self, chest_type: str = "basic_chest", num_items: int = 2) -> List[LootItem]:
        """Génère du butin pour un coffre."""
        table = self.get_table(chest_type)
        if table:
            return table.generate_loot(num_items)
        return []
    
    def generate_enemy_loot(self, enemy_type: str = "enemy_basic") -> List[LootItem]:
        """Génère du butin pour un ennemi vaincu."""
        table = self.get_table(enemy_type)
        if table:
            return table.generate_loot(1)
        return []


# Instance globale du générateur de butin
loot_generator = LootGenerator()