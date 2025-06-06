"""
Système de coffres interactifs.
"""
import pygame
from typing import List, Optional

from game.world.game_object import GameObject
from game.world.loot import LootItem, loot_generator


class ChestObject(GameObject):
    """Coffre interactif contenant du butin."""
    
    def __init__(
        self,
        x: float,
        y: float,
        chest_type: str = "basic_chest",
        sprite_path: str = "assets/sprites/chest.png"
    ):
        # Les coffres font 32x32 pixels (1 tile)
        super().__init__(
            name="chest",
            x=x,
            y=y,
            width=32,
            height=32,
            sprite_path=sprite_path,
            walkable=True  # Le joueur peut marcher sur les coffres
        )
        
        self.chest_type = chest_type
        self.is_opened = False
        self.loot: List[LootItem] = []
        self.interaction_radius = 40  # Distance pour interaction
        
        # Générer le butin à la création
        self._generate_loot()
        
        # Sprites pour coffre fermé/ouvert (pour plus tard)
        self.closed_sprite = self.sprite_surface
        self.opened_sprite = None  # TODO: Charger sprite coffre ouvert
    
    def _generate_loot(self):
        """Génère le butin du coffre selon son type."""
        if self.chest_type == "basic_chest":
            self.loot = loot_generator.generate_chest_loot("basic_chest", num_items=2)
        elif self.chest_type == "rare_chest":
            self.loot = loot_generator.generate_chest_loot("rare_chest", num_items=3)
        elif self.chest_type == "legendary_chest":
            self.loot = loot_generator.generate_chest_loot("legendary_chest", num_items=4)
        else:
            # Par défaut, coffre de base
            self.loot = loot_generator.generate_chest_loot("basic_chest", num_items=2)
    
    def can_interact_with(self, player_x: float, player_y: float) -> bool:
        """Vérifie si le joueur peut interagir avec ce coffre."""
        if self.is_opened:
            return False
        
        # Calculer la distance entre le joueur et le centre du coffre
        chest_center_x = self.x + self.width / 2
        chest_center_y = self.y + self.height / 2
        
        # Distance euclidienne
        dx = player_x - chest_center_x
        dy = player_y - chest_center_y
        distance = (dx * dx + dy * dy) ** 0.5
        
        return distance <= self.interaction_radius
    
    def open(self, player) -> List[LootItem]:
        """Ouvre le coffre et transfère le butin au joueur."""
        if self.is_opened:
            return []
        
        self.is_opened = True
        
        # Donner le butin au joueur
        received_loot = []
        total_gold = 0
        
        for loot_item in self.loot:
            if loot_item.item_type == "gold":
                total_gold += loot_item.item_data
            elif loot_item.item_type == "weapon":
                # Ajouter l'arme à l'inventaire du joueur
                if player.inventory.add_item(loot_item.item_data):
                    received_loot.append(loot_item)
            else:
                # Autres types d'objets (à implémenter plus tard)
                received_loot.append(loot_item)
        
        # Donner l'or au joueur (quand le système d'or sera implémenté)
        if total_gold > 0:
            # Pour l'instant, on simule en ajoutant à l'XP
            player.gain_experience(total_gold)
            received_loot.append(LootItem("gold", total_gold))
        
        # Mettre à jour le sprite (pour plus tard)
        if self.opened_sprite:
            self.sprite_surface = self.opened_sprite
        
        return received_loot
    
    def get_interaction_prompt(self) -> str:
        """Retourne le texte d'interaction à afficher."""
        if self.is_opened:
            return "Coffre vide"
        return "Appuyez sur E pour ouvrir"
    
    def render(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Affiche le coffre avec un indicateur d'interaction si nécessaire."""
        # Afficher le sprite du coffre
        super().render(screen, camera_x, camera_y)
        
        # TODO: Afficher un indicateur visuel si le coffre peut être ouvert
        # (par exemple, un contour doré ou une icône au-dessus)
    
    def get_loot_summary(self) -> str:
        """Retourne un résumé du butin pour le debug."""
        if not self.loot:
            return "Aucun butin"
        
        summary = []
        for item in self.loot:
            summary.append(str(item))
        
        return ", ".join(summary)


class ChestManager:
    """Gestionnaire pour tous les coffres du jeu."""
    
    def __init__(self):
        self.chests: List[ChestObject] = []
    
    def add_chest(self, chest: ChestObject):
        """Ajoute un coffre au gestionnaire."""
        self.chests.append(chest)
    
    def create_chest(self, x: float, y: float, chest_type: str = "basic_chest") -> ChestObject:
        """Crée et ajoute un nouveau coffre."""
        chest = ChestObject(x, y, chest_type)
        self.add_chest(chest)
        return chest
    
    def find_interactable_chest(self, player_x: float, player_y: float) -> Optional[ChestObject]:
        """Trouve le coffre le plus proche avec lequel le joueur peut interagir."""
        closest_chest = None
        closest_distance = float('inf')
        
        for chest in self.chests:
            if chest.can_interact_with(player_x, player_y):
                # Calculer la distance exacte pour trouver le plus proche
                chest_center_x = chest.x + chest.width / 2
                chest_center_y = chest.y + chest.height / 2
                dx = player_x - chest_center_x
                dy = player_y - chest_center_y
                distance = (dx * dx + dy * dy) ** 0.5
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_chest = chest
        
        return closest_chest
    
    def update(self, dt: float):
        """Met à jour tous les coffres (pour animations futures)."""
        for chest in self.chests:
            # TODO: Mettre à jour les animations d'ouverture
            pass
    
    def render_all(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Affiche tous les coffres."""
        for chest in self.chests:
            chest.render(screen, camera_x, camera_y)
    
    def get_stats(self) -> dict:
        """Retourne des statistiques sur les coffres."""
        total_chests = len(self.chests)
        opened_chests = sum(1 for chest in self.chests if chest.is_opened)
        
        return {
            "total_chests": total_chests,
            "opened_chests": opened_chests,
            "remaining_chests": total_chests - opened_chests
        }