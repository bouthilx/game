from typing import List, Optional, Dict, Any
from .weapon import Weapon


class Inventory:
    """Système d'inventaire simple pour le joueur."""
    
    def __init__(self, max_size: int = 20, owner=None):
        self.max_size = max_size
        self.items: List[Weapon] = []
        self.equipped_weapon: Optional[Weapon] = None
        self.owner = owner
    
    def add_item(self, item: Weapon) -> bool:
        """Ajoute un objet à l'inventaire. Retourne True si succès."""
        if len(self.items) >= self.max_size:
            return False  # Inventaire plein
        
        self.items.append(item)
        return True
    
    def remove_item(self, item: Weapon) -> bool:
        """Retire un objet de l'inventaire. Retourne True si succès."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def equip_weapon(self, weapon: Weapon) -> bool:
        """Équipe une arme. Retourne True si succès."""
        if weapon not in self.items:
            return False  # L'arme n'est pas dans l'inventaire
        
        # Déséquiper l'arme actuelle si elle existe
        if self.equipped_weapon:
            self.unequip_weapon()
        
        self.equipped_weapon = weapon
        return True
    
    def unequip_weapon(self) -> Optional[Weapon]:
        """Déséquipe l'arme actuelle. Retourne l'arme déséquipée."""
        if self.equipped_weapon:
            weapon = self.equipped_weapon
            self.equipped_weapon = None
            return weapon
        return None
    
    def get_equipped_weapon(self) -> Optional[Weapon]:
        """Retourne l'arme actuellement équipée."""
        return self.equipped_weapon
    
    def get_weapons(self) -> List[Weapon]:
        """Retourne toutes les armes dans l'inventaire."""
        return [item for item in self.items if isinstance(item, Weapon)]
    
    def get_available_weapons(self) -> List[Weapon]:
        """Retourne les armes non équipées."""
        weapons = self.get_weapons()
        if self.equipped_weapon in weapons:
            weapons.remove(self.equipped_weapon)
        return weapons
    
    def is_full(self) -> bool:
        """Vérifie si l'inventaire est plein."""
        return len(self.items) >= self.max_size
    
    def get_item_count(self) -> int:
        """Retourne le nombre d'objets dans l'inventaire."""
        return len(self.items)
    
    def get_inventory_info(self) -> Dict[str, Any]:
        """Retourne les informations de l'inventaire."""
        return {
            "items_count": len(self.items),
            "max_size": self.max_size,
            "equipped_weapon": self.equipped_weapon.name if self.equipped_weapon else None,
            "weapons": [weapon.name for weapon in self.get_weapons()]
        }