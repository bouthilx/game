from abc import ABC, abstractmethod
from typing import Dict, Any


class Weapon(ABC):
    """Classe de base pour toutes les armes."""
    
    def __init__(self, name: str, damage: int, description: str = ""):
        self.name = name
        self.damage = damage
        self.description = description
        self.weapon_type = "weapon"
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de l'arme."""
        return {
            "name": self.name,
            "damage": self.damage,
            "type": self.weapon_type,
            "description": self.description
        }
    
    def __str__(self) -> str:
        return f"{self.name} (Dégâts: {self.damage})"


class Sword(Weapon):
    """Arme de mêlée - Épée."""
    
    def __init__(self, name: str, damage: int, description: str = ""):
        super().__init__(name, damage, description)
        self.weapon_type = "sword"


# Épées prédéfinies selon GUIDELINES.md
class BasicSword(Sword):
    """Épée de base - arme de départ."""
    
    def __init__(self):
        super().__init__(
            name="Épée de Base",
            damage=20,
            description="Une épée simple mais efficace"
        )


class SteelSword(Sword):
    """Épée renforcée - amélioration intermédiaire."""
    
    def __init__(self):
        super().__init__(
            name="Épée d'Acier",
            damage=35,
            description="Une épée forgée dans l'acier de qualité"
        )


class LegendarySword(Sword):
    """Épée légendaire - arme de fin de jeu."""
    
    def __init__(self):
        super().__init__(
            name="Épée Légendaire",
            damage=50,
            description="Une lame forgée par les maîtres artisans"
        )


class Staff(Weapon):
    """Arme magique - Bâton."""
    
    def __init__(self, name: str, damage: int, description: str = ""):
        super().__init__(name, damage, description)
        self.weapon_type = "magic"


class MagicStaff(Staff):
    """Bâton magique - arme de mage."""
    
    def __init__(self):
        super().__init__(
            name="Bâton Magique",
            damage=30,
            description="Un bâton imprégné de magie ancienne"
        )


class Bow(Weapon):
    """Arme à distance - Arc."""
    
    def __init__(self, name: str, damage: int, description: str = ""):
        super().__init__(name, damage, description)
        self.weapon_type = "bow"


class ElvenBow(Bow):
    """Arc elfique - arme à distance précise."""
    
    def __init__(self):
        super().__init__(
            name="Arc Elfique",
            damage=25,
            description="Un arc léger et précis des forêts elfiques"
        )