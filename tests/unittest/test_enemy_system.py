import pytest
import pygame
from unittest.mock import Mock

from game.entities.enemy import Enemy, Goblin
from game.entities.player import Player


class TestEnemySystem:
    """Tests du système d'ennemis."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.enemy = Enemy(100, 100)
        self.goblin = Goblin(200, 200)
        self.player = Player(150, 150)
    
    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_enemy_basic_attributes(self):
        """L'ennemi a tous les attributs de base."""
        assert self.enemy.health == 30
        assert self.enemy.max_health == 30
        assert self.enemy.attack_damage == 10
        assert self.enemy.speed == 50.0
        assert self.enemy.experience_value == 25
        assert self.enemy.is_alive is True
        assert self.enemy.ai_state == "idle"

    def test_goblin_specialized_attributes(self):
        """Le gobelin a des stats spécialisées."""
        assert self.goblin.health == 20
        assert self.goblin.max_health == 20
        assert self.goblin.speed == 80.0
        assert self.goblin.attack_damage == 8
        assert self.goblin.experience_value == 15
        assert self.goblin.width == 24  # Plus petit
        assert self.goblin.height == 24

    def test_take_damage(self):
        """Test du système de dégâts."""
        # Dégâts normaux
        died = self.enemy.take_damage(10)
        assert self.enemy.health == 20
        assert died is False
        assert self.enemy.is_alive is True
        
        # Dégâts mortels
        died = self.enemy.take_damage(25)
        assert self.enemy.health == 0
        assert died is True
        assert self.enemy.is_alive is False
        
        # Pas de dégâts sur ennemi mort
        died = self.enemy.take_damage(10)
        assert died is False
        assert self.enemy.health == 0

    def test_distance_to_target(self):
        """Test du calcul de distance."""
        self.enemy.target = self.player
        
        # Distance attendue: sqrt((150-100)² + (150-100)²) = sqrt(2500 + 2500) ≈ 70.71
        distance = self.enemy.distance_to_target()
        assert abs(distance - 70.71) < 0.1
        
        # Sans cible
        self.enemy.target = None
        assert self.enemy.distance_to_target() == float('inf')

    def test_can_attack_cooldown(self):
        """Test du cooldown d'attaque ennemi."""
        current_time = 0
        assert self.enemy.can_attack(current_time) is True
        
        # Après attaque
        self.enemy.last_attack_time = current_time
        assert self.enemy.can_attack(current_time) is False
        
        # Après cooldown
        current_time += self.enemy.attack_cooldown + 0.1
        assert self.enemy.can_attack(current_time) is True

    def test_ai_state_transitions(self):
        """Test des transitions d'état de l'IA."""
        self.enemy.target = self.player
        current_time = 0
        
        # État initial: idle
        assert self.enemy.ai_state == "idle"
        
        # Joueur entre dans le rayon de détection
        self.player.x = self.enemy.x + 50  # Distance < detection_radius (100)
        self.player.y = self.enemy.y + 50
        self.enemy.update_ai(0.1, current_time)
        assert self.enemy.ai_state == "chase"
        
        # Joueur entre dans le rayon d'attaque
        self.player.x = self.enemy.x + 20  # Distance < attack_range (35)
        self.player.y = self.enemy.y + 20
        self.enemy.update_ai(0.1, current_time)
        assert self.enemy.ai_state == "attack"
        
        # Joueur sort du rayon d'attaque
        self.player.x = self.enemy.x + 50
        self.player.y = self.enemy.y + 50
        self.enemy.update_ai(0.1, current_time)
        assert self.enemy.ai_state == "chase"

    def test_move_towards_target(self):
        """Test du mouvement vers la cible."""
        self.enemy.target = self.player
        
        # Joueur à droite et en bas
        self.player.x = self.enemy.x + 100
        self.player.y = self.enemy.y + 100
        
        self.enemy.move_towards_target(1.0)
        
        # Vélocité devrait être positive dans les deux directions
        assert self.enemy.velocity_x > 0
        assert self.enemy.velocity_y > 0
        assert abs(self.enemy.velocity_x) <= self.enemy.speed
        assert abs(self.enemy.velocity_y) <= self.enemy.speed

    def test_attack_target(self):
        """Test de l'attaque sur la cible."""
        self.enemy.target = self.player
        initial_health = self.player.health
        
        # Placer le joueur dans le rayon d'attaque
        self.player.x = self.enemy.x + 20
        self.player.y = self.enemy.y + 20
        
        current_time = 0
        self.enemy.attack_target(current_time)
        
        # Le joueur devrait avoir pris des dégâts
        assert self.player.health == initial_health - self.enemy.attack_damage
        assert self.enemy.last_attack_time == current_time

    def test_attack_target_out_of_range(self):
        """L'attaque ne fonctionne pas hors de portée."""
        self.enemy.target = self.player
        initial_health = self.player.health
        
        # Placer le joueur hors du rayon d'attaque
        self.player.x = self.enemy.x + 100
        self.player.y = self.enemy.y + 100
        
        current_time = 0
        self.enemy.attack_target(current_time)
        
        # Le joueur ne devrait pas avoir pris de dégâts
        assert self.player.health == initial_health
        assert self.enemy.last_attack_time == -1  # Pas d'attaque (valeur initiale)

    def test_check_collision_with_attack(self):
        """Test de collision avec attaque du joueur."""
        # Attack rect qui touche l'ennemi
        attack_rect = pygame.Rect(self.enemy.x, self.enemy.y, 40, 40)
        assert self.enemy.check_collision_with_attack(attack_rect) is True
        
        # Attack rect qui ne touche pas
        attack_rect = pygame.Rect(self.enemy.x + 100, self.enemy.y + 100, 40, 40)
        assert self.enemy.check_collision_with_attack(attack_rect) is False
        
        # Ennemi mort ne peut pas être touché
        self.enemy.is_alive = False
        attack_rect = pygame.Rect(self.enemy.x, self.enemy.y, 40, 40)
        assert self.enemy.check_collision_with_attack(attack_rect) is False

    def test_update_stops_when_dead(self):
        """L'update s'arrête quand l'ennemi est mort."""
        self.enemy.target = self.player
        self.enemy.is_alive = False
        
        initial_velocity_x = self.enemy.velocity_x
        initial_velocity_y = self.enemy.velocity_y
        
        self.enemy.update(1.0, 0)
        
        # Pas de changement de vélocité
        assert self.enemy.velocity_x == initial_velocity_x
        assert self.enemy.velocity_y == initial_velocity_y

    def test_full_ai_cycle(self):
        """Test d'un cycle complet d'IA."""
        self.enemy.target = self.player
        current_time = 0
        
        # Placer le joueur dans le rayon de détection mais pas d'attaque
        # Enemy: (100, 100), Player: (180, 180) -> distance = sqrt(80² + 80²) ≈ 113
        # Mais detection_radius = 100, donc il faut réduire la distance
        self.player.x = self.enemy.x + 60  # Distance ≈ 85 < 100
        self.player.y = self.enemy.y + 60
        
        # Vérifier la distance calculée
        distance = self.enemy.distance_to_target()
        assert distance < self.enemy.detection_radius
        assert distance > self.enemy.attack_range  # Dans la zone chase, pas attack
        
        # Appeler update_ai directement pour tester l'IA
        self.enemy.update_ai(1.0, current_time)
        
        assert self.enemy.ai_state == "chase"
        
        # Test directement move_towards_target pour vérifier le mouvement
        self.enemy.move_towards_target(1.0)
        
        # L'ennemi devrait avoir une vélocité vers le joueur
        assert self.enemy.velocity_x > 0  # Vers la droite
        assert self.enemy.velocity_y > 0  # Vers le bas


class TestPlayerEnemyInteraction:
    """Tests des interactions joueur-ennemi."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.player = Player(100, 100)
        self.enemies = [Goblin(150, 100), Goblin(200, 100)]
    
    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_player_attack_hits_enemy(self):
        """L'attaque du joueur touche l'ennemi."""
        # Mettre le joueur en état d'attaque vers la droite
        self.player.facing_direction = "right"
        self.player.is_attacking = True
        
        hit_enemies = self.player.check_attack_hits(self.enemies)
        assert len(hit_enemies) == 1
        assert hit_enemies[0] == self.enemies[0]  # Le plus proche

    def test_player_deal_damage_gives_xp(self):
        """Tuer un ennemi donne de l'XP."""
        # Mettre l'ennemi en état critique
        self.enemies[0].health = 5
        
        # Attaquer
        self.player.facing_direction = "right"
        self.player.is_attacking = True
        
        initial_xp = self.player.experience
        xp_gained = self.player.deal_damage_to_enemies(self.enemies)
        
        assert xp_gained == self.enemies[0].experience_value
        assert not self.enemies[0].is_alive

    def test_no_double_damage_same_attack(self):
        """Un ennemi ne prend des dégâts qu'une fois par attaque."""
        enemy = self.enemies[0]
        initial_health = enemy.health
        
        # Commencer une attaque
        self.player.start_attack(0)
        self.player.facing_direction = "right"
        
        # Premier coup
        xp1 = self.player.deal_damage_to_enemies(self.enemies)
        health_after_first = enemy.health
        
        # Deuxième appel dans la même attaque
        xp2 = self.player.deal_damage_to_enemies(self.enemies)
        health_after_second = enemy.health
        
        # Santé ne devrait pas avoir changé au deuxième appel
        assert health_after_first == health_after_second
        assert health_after_first == initial_health - self.player.attack_damage
        assert xp2 == 0  # Pas d'XP supplémentaire