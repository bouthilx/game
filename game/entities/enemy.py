import pygame
import math

from game.entities.entity import Entity


class Enemy(Entity):
    """Classe de base pour tous les ennemis."""
    
    def __init__(self, x: float, y: float, width: int = 32, height: int = 32):
        super().__init__(x, y, width, height)
        
        # Stats de base
        self.health = 30
        self.max_health = 30
        self.attack_damage = 10
        self.speed = 50.0
        self.experience_value = 25  # XP donné quand tué
        
        # IA de base
        self.target = None  # Joueur ciblé
        self.detection_radius = 100
        self.attack_range = 35
        self.last_attack_time = -1  # Initialize to -1 so first attack works
        self.attack_cooldown = 1.0  # seconds
        
        # État
        self.is_alive = True
        self.ai_state = "idle"  # idle, chase, attack
        
        # Couleur pour rendu (sera remplacée par sprites)
        self.color = (255, 100, 100)  # Rouge pour ennemi
    
    def take_damage(self, damage: int) -> bool:
        """Prend des dégâts. Retourne True si l'ennemi meurt."""
        if not self.is_alive:
            return False
            
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.is_alive = False
            return True
        return False
    
    def can_attack(self, current_time: float) -> bool:
        """Vérifie si l'ennemi peut attaquer."""
        return current_time - self.last_attack_time >= self.attack_cooldown
    
    def distance_to_target(self) -> float:
        """Calcule la distance au joueur cible."""
        if not self.target:
            return float('inf')
        
        # Calculer distance entre centres des entités
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        target_center_x = self.target.x + self.target.width / 2
        target_center_y = self.target.y + self.target.height / 2
        
        dx = target_center_x - center_x
        dy = target_center_y - center_y
        return math.sqrt(dx * dx + dy * dy)
    
    def move_towards_target(self, dt: float):
        """Déplace l'ennemi vers sa cible."""
        if not self.target:
            return
        
        # Utiliser les centres comme dans distance_to_target pour cohérence
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        target_center_x = self.target.x + self.target.width / 2
        target_center_y = self.target.y + self.target.height / 2
        
        dx = target_center_x - center_x
        dy = target_center_y - center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Normaliser la direction
            dx /= distance
            dy /= distance
            
            # Appliquer la vitesse
            self.velocity_x = dx * self.speed
            self.velocity_y = dy * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def update_ai(self, dt: float, current_time: float):
        """Met à jour l'IA de l'ennemi."""
        if not self.is_alive:
            return
        
        distance_to_player = self.distance_to_target()
        
        # Machine d'état simple
        if self.ai_state == "idle":
            if distance_to_player <= self.detection_radius:
                self.ai_state = "chase"
        
        elif self.ai_state == "chase":
            if distance_to_player <= self.attack_range:
                self.ai_state = "attack"
            elif distance_to_player > self.detection_radius * 1.5:  # Perd la cible
                self.ai_state = "idle"
                self.velocity_x = 0
                self.velocity_y = 0
            else:
                self.move_towards_target(dt)
        
        elif self.ai_state == "attack":
            if distance_to_player > self.attack_range:
                self.ai_state = "chase"
            else:
                # Arrêter le mouvement pour attaquer
                self.velocity_x = 0
                self.velocity_y = 0
                # Attaquer si possible
                if self.can_attack(current_time):
                    self.attack_target(current_time)
    
    def attack_target(self, current_time: float):
        """Attaque le joueur cible."""
        if self.target and self.distance_to_target() <= self.attack_range:
            self.target.take_damage(self.attack_damage)
            self.last_attack_time = current_time
    
    def check_collision_with_attack(self, attack_rect: pygame.Rect) -> bool:
        """Vérifie si l'ennemi est touché par une attaque."""
        if not self.is_alive:
            return False
        return self.rect.colliderect(attack_rect)
    
    def update(self, dt: float, current_time: float = 0):
        """Met à jour l'ennemi."""
        if not self.is_alive:
            return
        
        # Mettre à jour l'IA
        self.update_ai(dt, current_time)
        
        # Appliquer le mouvement (hérité de Entity)
        super().update(dt)
    
    def render(self, screen: pygame.Surface):
        """Affiche l'ennemi."""
        if not self.is_alive:
            return
        
        # Dessiner l'ennemi (couleur selon état)
        color = self.color
        if self.ai_state == "chase":
            color = (255, 150, 150)  # Plus clair quand en poursuite
        elif self.ai_state == "attack":
            color = (255, 0, 0)  # Rouge vif quand attaque
        
        pygame.draw.rect(screen, color, self.rect)
        
        # Barre de vie
        if self.health < self.max_health:
            health_bar_width = 30
            health_bar_height = 4
            health_percentage = self.health / self.max_health
            
            # Fond rouge
            health_bg = pygame.Rect(
                self.x, self.y - 8, health_bar_width, health_bar_height
            )
            pygame.draw.rect(screen, (100, 0, 0), health_bg)
            
            # Barre verte
            health_fill = pygame.Rect(
                self.x, self.y - 8, 
                int(health_bar_width * health_percentage), health_bar_height
            )
            pygame.draw.rect(screen, (0, 255, 0), health_fill)


class Goblin(Enemy):
    """Ennemi Gobelin - rapide avec peu de vie."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 24, 24)  # Plus petit
        
        # Stats spécifiques au gobelin
        self.health = 20
        self.max_health = 20
        self.speed = 80.0  # Plus rapide
        self.attack_damage = 8  # Moins de dégâts
        self.experience_value = 15  # Moins d'XP
        self.attack_cooldown = 0.8  # Attaque plus souvent
        
        # Couleur spécifique
        self.color = (100, 255, 100)  # Vert pour gobelin