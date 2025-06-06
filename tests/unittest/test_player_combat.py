import pytest
import pygame
from unittest.mock import Mock, patch
from collections import defaultdict

from game.entities.player import Player


class TestPlayerCombat:
    """Test du système de combat du joueur."""

    def setup_method(self):
        """Setup pour chaque test."""
        pygame.init()
        self.player = Player(100, 100)
    
    def teardown_method(self):
        """Cleanup après chaque test."""
        pygame.quit()

    def test_player_has_combat_attributes(self):
        """Le joueur a tous les attributs de combat."""
        assert hasattr(self.player, 'base_attack_damage')
        assert hasattr(self.player, 'attack_range')
        assert hasattr(self.player, 'attack_cooldown')
        assert hasattr(self.player, 'facing_direction')
        assert hasattr(self.player, 'is_attacking')
        
        # Player now has equipment system so total damage includes weapon
        assert self.player.get_attack_damage() == 30  # 10 base + 20 from BasicSword
        assert self.player.attack_range == 40
        assert self.player.attack_cooldown == 0.5
        assert self.player.facing_direction == "down"
        assert self.player.is_attacking is False

    def test_can_attack_cooldown(self):
        """Test du système de cooldown d'attaque."""
        current_time = 0
        
        # Peut attaquer au début
        assert self.player.can_attack(current_time) is True
        
        # Après une attaque, cooldown actif
        self.player.start_attack(current_time)
        assert self.player.can_attack(current_time) is False
        
        # Après le cooldown, peut attaquer à nouveau
        current_time += self.player.attack_cooldown + 0.1
        assert self.player.can_attack(current_time) is True

    def test_start_attack(self):
        """Test du démarrage d'attaque."""
        current_time = 5.0
        
        self.player.start_attack(current_time)
        
        assert self.player.is_attacking is True
        assert self.player.attack_start_time == current_time
        assert self.player.last_attack_time == current_time

    def test_attack_state_update(self):
        """Test de la mise à jour de l'état d'attaque."""
        current_time = 0
        
        # Commencer une attaque
        self.player.start_attack(current_time)
        assert self.player.is_attacking is True
        
        # Pendant l'animation
        self.player.update_attack_state(current_time + 0.1)
        assert self.player.is_attacking is True
        
        # Après l'animation
        self.player.update_attack_state(current_time + self.player.attack_animation_time + 0.1)
        assert self.player.is_attacking is False

    def test_facing_direction_changes_with_movement(self):
        """La direction change avec le mouvement."""
        with patch('pygame.key.get_pressed') as mock_keys:
            # Create key state that returns False by default
            key_state = defaultdict(bool)
            
            # Mouvement vers la droite
            key_state[pygame.K_RIGHT] = True
            mock_keys.return_value = key_state
            
            self.player.handle_input(0)
            assert self.player.facing_direction == "right"
            
            # Mouvement vers la gauche
            key_state[pygame.K_RIGHT] = False
            key_state[pygame.K_LEFT] = True
            
            self.player.handle_input(0)
            assert self.player.facing_direction == "left"

    def test_get_attack_rect_different_directions(self):
        """Test des rectangles d'attaque selon les directions."""
        player_x, player_y = self.player.x, self.player.y
        
        # Test attaque vers la droite
        self.player.facing_direction = "right"
        self.player.is_attacking = True
        attack_rect = self.player.get_attack_rect()
        
        assert attack_rect.x == player_x + self.player.width
        assert attack_rect.width == self.player.attack_range
        assert attack_rect.height == self.player.attack_range
        
        # Test attaque vers la gauche
        self.player.facing_direction = "left"
        attack_rect = self.player.get_attack_rect()
        
        assert attack_rect.x == player_x - self.player.attack_range
        
        # Test attaque vers le bas
        self.player.facing_direction = "down"
        attack_rect = self.player.get_attack_rect()
        
        assert attack_rect.y == player_y + self.player.height
        
        # Test attaque vers le haut
        self.player.facing_direction = "up"
        attack_rect = self.player.get_attack_rect()
        
        assert attack_rect.y == player_y - self.player.attack_range

    def test_get_attack_rect_when_not_attacking(self):
        """Pas de rectangle d'attaque quand pas en train d'attaquer."""
        self.player.is_attacking = False
        attack_rect = self.player.get_attack_rect()
        
        assert attack_rect.width == 0
        assert attack_rect.height == 0

    @patch('pygame.key.get_pressed')
    def test_space_key_triggers_attack(self, mock_keys):
        """La touche espace déclenche une attaque."""
        # Create key state that returns False by default
        key_state = defaultdict(bool)
        key_state[pygame.K_SPACE] = True
        
        mock_keys.return_value = key_state
        
        current_time = 0
        self.player.handle_input(current_time)
        
        assert self.player.is_attacking is True
        assert self.player.last_attack_time == current_time

    def test_attack_during_cooldown_ignored(self):
        """Les attaques pendant le cooldown sont ignorées."""
        with patch('pygame.key.get_pressed') as mock_keys:
            # Create key state that returns False by default
            key_state = defaultdict(bool)
            key_state[pygame.K_SPACE] = True
            mock_keys.return_value = key_state
            
            current_time = 0
            
            # Première attaque
            self.player.handle_input(current_time)
            first_attack_time = self.player.last_attack_time
            
            # Tentative d'attaque immédiate (devrait être ignorée)
            current_time += 0.1  # Moins que le cooldown
            self.player.handle_input(current_time)
            
            # Le temps de dernière attaque ne devrait pas avoir changé
            assert self.player.last_attack_time == first_attack_time