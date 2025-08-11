import pygame
import math

from .animated_entity import AnimatedEntity, AnimationState


class Enemy(AnimatedEntity):
    """Classe de base pour tous les ennemis."""
    
    def __init__(
        self, 
        x: float, 
        y: float, 
        width: int = 32, 
        height: int = 32,
        sprite_sheet_path: str = None,
        fallback_color: tuple[int, int, int] = (128, 128, 128)
    ):
        super().__init__(x, y, width, height, sprite_sheet_path, fallback_color)
        
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
        self.is_corpse = False  # True when death animation finished
        self.ai_state = "idle"  # idle, chase, attack
        
        # Blood puddle system
        self.corpse_time = 0.0  # Time since becoming a corpse
        self.blood_puddle_max_time = 3.0  # Time for puddle to reach full size
        self.blood_color = (50, 150, 50, 180)  # Green blood with alpha
        self.blood_puddle_shape = None  # Pre-generated puddle shape for consistency
        
        # Couleur pour rendu (sera remplacée par sprites)
        self.color = (255, 100, 100)  # Rouge pour ennemi
    
    def take_damage(self, damage: int) -> bool:
        """Prend des dégâts. Retourne True si l'ennemi commence à mourir."""
        if not self.is_alive:
            return False
            
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.is_alive = False  # Start dying
            self.velocity_x = 0  # Stop moving immediately
            self.velocity_y = 0
            self._death_start_time = 0.0  # Will be set in update with current_time
            self._debug_id = id(self)  # Add debug ID for tracking BEFORE playing animation
            self.play_death_animation()  # Play death animation
            print(f"DEATH: Enemy {id(self)} died at ({self.x:.0f}, {self.y:.0f}), animation_state={self.animation_state.value}")
            return True  # Started dying process
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
    
    def can_move_to(self, x: float, y: float, game_map, chest_manager=None, player=None, other_enemies=None) -> bool:
        """Check if enemy can move to the specified position."""
        if not game_map:
            return True  # No collision checking if no map provided
        
        margin = 2
        corners = [
            (x + margin, y + margin),
            (x + self.width - margin, y + margin),
            (x + margin, y + self.height - margin),
            (x + self.width - margin, y + self.height - margin),
        ]

        # Check terrain walkability
        for corner_x, corner_y in corners:
            if not game_map.is_walkable(corner_x, corner_y):
                return False
        
        # Create a rect for the new position
        enemy_rect = pygame.Rect(x, y, self.width, self.height)
        
        # Check chest collisions if chest_manager provided
        if chest_manager:
            for chest in chest_manager.chests:
                if enemy_rect.colliderect(chest.rect):
                    return False
        
        # Check player collision if player provided
        if player:
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            if enemy_rect.colliderect(player_rect):
                return False
        
        # Check other enemies collision if provided
        if other_enemies:
            for other_enemy in other_enemies:
                # Don't check collision with self
                if other_enemy is self:
                    continue
                
                # Only check collision with living enemies (corpses don't block movement)
                if other_enemy.blocks_movement():
                    other_rect = pygame.Rect(other_enemy.x, other_enemy.y, other_enemy.width, other_enemy.height)
                    if enemy_rect.colliderect(other_rect):
                        return False
        
        return True
    
    def move_towards_target(self, dt: float, game_map=None, chest_manager=None, player=None, other_enemies=None):
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
            
            # Calculate desired velocity
            desired_vel_x = dx * self.speed
            desired_vel_y = dy * self.speed
            
            # Check collision before applying movement
            if self.can_move_to(
                self.x + desired_vel_x * dt,
                self.y + desired_vel_y * dt,
                game_map,
                chest_manager,
                player,
                other_enemies
            ):
                self.velocity_x = desired_vel_x
                self.velocity_y = desired_vel_y
            else:
                # Try moving only horizontally
                if self.can_move_to(
                    self.x + desired_vel_x * dt,
                    self.y,
                    game_map,
                    chest_manager,
                    player,
                    other_enemies
                ):
                    self.velocity_x = desired_vel_x
                    self.velocity_y = 0
                # Try moving only vertically
                elif self.can_move_to(
                    self.x,
                    self.y + desired_vel_y * dt,
                    game_map,
                    chest_manager,
                    player,
                    other_enemies
                ):
                    self.velocity_x = 0
                    self.velocity_y = desired_vel_y
                else:
                    # Can't move in either direction
                    self.velocity_x = 0
                    self.velocity_y = 0
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        # Update animation based on movement (only if alive)
        if self.is_alive:
            self.update_movement_animation(self.velocity_x, self.velocity_y)
    
    def update_ai(self, dt: float, current_time: float, game_map=None, chest_manager=None, player=None, other_enemies=None):
        """Met à jour l'IA de l'ennemi."""
        if not self.is_alive:
            # Dead enemies should not move or update AI
            self.velocity_x = 0
            self.velocity_y = 0
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
                self.move_towards_target(dt, game_map, chest_manager, player, other_enemies)
        
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
            # Play attack animation
            self.play_attack_animation()
    
    def check_collision_with_attack(self, attack_rect: pygame.Rect) -> bool:
        """Vérifie si l'ennemi est touché par une attaque."""
        if not self.is_alive or self.is_corpse:
            return False  # Can't attack dead or corpse enemies
        return self.rect.colliderect(attack_rect)
    
    def blocks_movement(self) -> bool:
        """Check if this enemy blocks movement. Corpses don't block."""
        return self.is_alive  # Only living enemies block movement
    
    def get_blood_puddle_size(self) -> float:
        """Get current blood puddle size as a percentage (0.0 to 1.0)."""
        if not self.is_corpse or self.corpse_time <= 0:
            return 0.0
        return min(1.0, self.corpse_time / self.blood_puddle_max_time)
    
    def _generate_blood_puddle_shape(self):
        """Pre-generate blood puddle shape for consistent rendering."""
        import random
        
        # Use enemy's initial position + ID as seed for consistency
        random.seed(int(self.x * 1000 + self.y * 1000 + id(self)))
        
        # Calculate maximum puddle dimensions
        max_puddle_width = int(self.width * 1.5)  # 150% of enemy width
        max_puddle_height = int(self.height * 1.2)  # 120% of enemy height
        
        # Generate blob data (relative positions and sizes)
        self.blood_puddle_shape = {
            'max_width': max_puddle_width,
            'max_height': max_puddle_height,
            'blobs': []
        }
        
        # Add main blob (always present)
        self.blood_puddle_shape['blobs'].append({
            'x_ratio': 0.0,  # Center
            'y_ratio': 0.0,  # Center
            'width_ratio': 1.0,  # Full width
            'height_ratio': 1.0,  # Full height
            'is_main': True
        })
        
        # Add smaller irregular blobs
        num_blobs = 4 + random.randint(0, 3)  # 4-7 total blobs
        for i in range(num_blobs):
            self.blood_puddle_shape['blobs'].append({
                'x_ratio': random.uniform(-0.3, 0.3),  # Relative to center
                'y_ratio': random.uniform(-0.3, 0.3),
                'width_ratio': random.uniform(0.3, 0.7),
                'height_ratio': random.uniform(0.3, 0.7),
                'is_main': False
            })
    
    def render_blood_puddle(self, screen: pygame.Surface):
        """Render growing blood puddle underneath corpse."""
        if not self.is_corpse or not self.blood_puddle_shape:
            return
        
        puddle_size = self.get_blood_puddle_size()
        if puddle_size <= 0:
            return
        
        max_width = self.blood_puddle_shape['max_width']
        max_height = self.blood_puddle_shape['max_height']
        
        current_width = int(max_width * puddle_size)
        current_height = int(max_height * puddle_size)
        
        if current_width <= 0 or current_height <= 0:
            return
        
        # Center puddle under the corpse
        puddle_x = self.x + (self.width - current_width) // 2
        puddle_y = self.y + (self.height - current_height) // 2
        
        # Create surface for this specific puddle size
        puddle_surface = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
        
        # Draw all blobs using pre-generated shape data
        for blob in self.blood_puddle_shape['blobs']:
            blob_width = int(current_width * blob['width_ratio'])
            blob_height = int(current_height * blob['height_ratio'])
            
            if blob_width <= 0 or blob_height <= 0:
                continue
            
            # Calculate position relative to center
            blob_x = int(current_width // 2 + blob['x_ratio'] * current_width - blob_width // 2)
            blob_y = int(current_height // 2 + blob['y_ratio'] * current_height - blob_height // 2)
            
            # Clamp to surface bounds
            blob_x = max(0, min(blob_x, current_width - blob_width))
            blob_y = max(0, min(blob_y, current_height - blob_height))
            
            pygame.draw.ellipse(puddle_surface, self.blood_color,
                               (blob_x, blob_y, blob_width, blob_height))
        
        # Blit the puddle to screen
        screen.blit(puddle_surface, (puddle_x, puddle_y))
    
    def update(self, dt: float, current_time: float = 0, game_map=None, chest_manager=None, player=None, other_enemies=None):
        """Met à jour l'ennemi."""
        # Always update animations (for death animation and corpses)
        self.update_animation(dt)
        
        # Check if death animation finished and convert to corpse
        if not self.is_alive and not self.is_corpse:
            # Set death start time on first update after death
            if hasattr(self, '_death_start_time') and self._death_start_time == 0.0:
                self._death_start_time = current_time
            
            # Add fallback: if dead for too long without finishing animation, force corpse state
            if hasattr(self, '_death_start_time') and self._death_start_time > 0:
                if current_time - self._death_start_time > 2.0:  # 2 seconds max for death
                    self.is_corpse = True
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.corpse_time = 0.0
                    self._generate_blood_puddle_shape()
            
            if self.is_death_animation_finished():
                self.is_corpse = True
                self.velocity_x = 0  # Stop any movement
                self.velocity_y = 0
                self.corpse_time = 0.0  # Start blood puddle timer
                self._generate_blood_puddle_shape()  # Pre-generate consistent shape
        
        # Update blood puddle growth for corpses
        if self.is_corpse:
            self.corpse_time += dt
        
        # Only do AI and movement if alive (not dead or corpse)
        if self.is_alive:
            # Store old position for animation
            old_x, old_y = self.x, self.y
            
            # Mettre à jour l'IA
            self.update_ai(dt, current_time, game_map, chest_manager, player, other_enemies)
            
            # Update movement animations based on velocity
            self.update_movement_animation(self.velocity_x, self.velocity_y)
            
            # Appliquer le mouvement (hérité de Entity)
            super().update(dt)
        else:
            # Dead enemies should not have walking animations
            # Make sure death animation is set properly if they're stuck in walk
            if not self.is_corpse and self.animation_state != AnimationState.DEATH:
                print(f"DEATH: Enemy {id(self)} at ({self.x:.0f}, {self.y:.0f}) stuck in {self.animation_state.value}, forcing death animation")
                self.play_death_animation()
                print(f"DEATH: After forcing, animation_state={self.animation_state.value}")
            
            # Log if dead enemy has velocity
            if self.velocity_x != 0 or self.velocity_y != 0:
                print(f"DEATH: Dead enemy {id(self)} has velocity ({self.velocity_x:.1f}, {self.velocity_y:.1f}), zeroing")
            
            # Ensure dead enemies have no velocity
            self.velocity_x = 0
            self.velocity_y = 0
    
    def render(self, screen: pygame.Surface):
        """Affiche l'ennemi."""
        # Render sprites for both alive enemies and corpses
        super().render(screen)
        
        # Only show health bar for living enemies
        if self.is_alive and self.health < self.max_health:
            health_bar_width = max(30, self.width)  # Au moins 30px, sinon largeur de l'ennemi
            health_bar_height = 6 if self.width > 32 else 4  # Plus grosse barre pour gros ennemis
            health_percentage = self.health / self.max_health
            
            # Centrer la barre de vie au-dessus de l'ennemi
            bar_x = self.x + (self.width - health_bar_width) // 2
            bar_y = self.y - health_bar_height - 4
            
            # Fond rouge
            health_bg = pygame.Rect(bar_x, bar_y, health_bar_width, health_bar_height)
            pygame.draw.rect(screen, (100, 0, 0), health_bg)
            
            # Barre verte
            health_fill = pygame.Rect(
                bar_x, bar_y, 
                int(health_bar_width * health_percentage), health_bar_height
            )
            pygame.draw.rect(screen, (0, 255, 0), health_fill)


class Goblin(Enemy):
    """Ennemi Gobelin - rapide avec peu de vie."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x, y, 32, 32,  # Use 32x32 to match sprite size
            sprite_sheet_path="characters/goblin/goblin_spritesheet.png",
            fallback_color=(100, 255, 100)  # Green fallback
        )
        
        # Stats spécifiques au gobelin
        self.health = 20
        self.max_health = 20
        self.speed = 80.0  # Plus rapide
        self.attack_damage = 8  # Moins de dégâts
        self.experience_value = 15  # Moins d'XP
        self.attack_cooldown = 0.8  # Attaque plus souvent
        
        # Goblin-specific green blood
        self.blood_color = (80, 200, 80, 160)  # Brighter green blood
        self.blood_puddle_max_time = 4.0  # Slightly longer for goblins


class Ogre(Enemy):
    """Ennemi Ogre - très résistant et plus gros."""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x, y, 64, 64,  # 2x plus gros (64x64 vs 32x32)
            sprite_sheet_path="characters/ogre/ogre_spritesheet.png",  # Will fall back to color for now
            fallback_color=(200, 100, 100)  # Rouge-brun pour ogre
        )
        
        # Stats spécifiques à l'ogre
        self.health = 100
        self.max_health = 100
        self.speed = 30.0  # Plus lent que les autres
        self.attack_damage = 20  # Dégâts élevés
        self.experience_value = 100  # Beaucoup d'XP
        self.attack_cooldown = 1.5  # Attaque plus lentement
        self.detection_radius = 120  # Détection légèrement meilleure
        self.attack_range = 50  # Portée d'attaque plus grande
        
        # Ogre-specific dark red blood
        self.blood_color = (120, 50, 50, 180)  # Dark red blood
        self.blood_puddle_max_time = 5.0  # Longer for bigger ogres