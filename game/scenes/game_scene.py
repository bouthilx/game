import pygame

from game.engine.scene import Scene
from game.entities.player import Player
from game.entities.enemy import Goblin, Ogre
from game.world.bitmap_map import BitmapMap
from game.world.chest import ChestManager


class GameScene(Scene):
    def __init__(self, map_path: str = "data/maps/large_map.png"):
        super().__init__()
        self.game_map = BitmapMap(map_path, tile_size=32)
        # Find a safe spawn position that avoids objects
        spawn_x, spawn_y = self.game_map.find_safe_spawn_position()
        self.player = Player(spawn_x, spawn_y)
        self.camera_x = 0
        self.camera_y = 0
        self.current_time = 0
        
        # Gestionnaire de coffres
        self.chest_manager = ChestManager()
        self.spawn_test_chests()
        
        # Créer quelques ennemis de test
        self.enemies = []
        self.spawn_test_enemies()

    def spawn_test_chests(self):
        """Spawn quelques coffres de test dans le monde."""
        player_x, player_y = self.player.x, self.player.y
        
        # Positions relatives au joueur pour spawner des coffres
        chest_positions = [
            # Coffres proches pour tester l'interaction
            (player_x + 200, player_y + 100, "basic_chest"),
            (player_x - 150, player_y + 200, "rare_chest"),
            (player_x + 300, player_y - 150, "basic_chest"),
            # Coffre légendaire plus loin
            (player_x + 500, player_y + 300, "legendary_chest"),
            (player_x - 400, player_y - 250, "rare_chest"),
        ]
        
        spawned_count = 0
        for x, y, chest_type in chest_positions:
            # Vérifier que la position est walkable
            if self.game_map.is_walkable(x, y):
                chest = self.chest_manager.create_chest(x, y, chest_type)
                spawned_count += 1
                print(f"Spawned {chest_type} at ({x}, {y}) - Contains: {chest.get_loot_summary()}")
        
        print(f"Spawned {spawned_count} chests total")

    def spawn_test_enemies(self):
        """Spawn quelques ennemis de test autour du joueur."""
        player_x, player_y = self.player.x, self.player.y
        
        # Spawn des ennemis à différentes distances (plus proches pour être visibles)
        enemy_positions = [
            # Très proches (immédiatement visibles)
            (player_x + 100, player_y + 80),
            (player_x + 80, player_y - 100),
            (player_x - 120, player_y + 60),
            (player_x - 80, player_y - 80),
            # Proches (dans le champ de vision)
            (player_x + 200, player_y + 150),
            (player_x + 150, player_y - 180),
            (player_x - 180, player_y + 120),
            (player_x - 150, player_y - 150),
            # Plus loin (pour tester la poursuite)
            (player_x + 350, player_y + 200),
            (player_x + 300, player_y - 250),
        ]
        
        spawned_count = 0
        ogre_count = 0
        for i, (x, y) in enumerate(enemy_positions):
            # Vérifier que la position est walkable
            if self.game_map.is_walkable(x, y):
                # Spawn un Ogre au milieu des ennemis (position 4) et un autre plus loin
                if i == 4 or i == 8:
                    # Vérifier que l'ogre (64x64) a assez de place
                    if (self.game_map.is_walkable(x + 32, y) and 
                        self.game_map.is_walkable(x, y + 32) and 
                        self.game_map.is_walkable(x + 32, y + 32)):
                        ogre = Ogre(x, y)
                        ogre.target = self.player
                        self.enemies.append(ogre)
                        ogre_count += 1
                        spawned_count += 1
                    else:
                        # Si pas de place pour l'ogre, spawn un gobelin
                        goblin = Goblin(x, y)
                        goblin.target = self.player
                        self.enemies.append(goblin)
                        spawned_count += 1
                else:
                    # Spawn un gobelin normal
                    goblin = Goblin(x, y)
                    goblin.target = self.player  # Cibler le joueur
                    self.enemies.append(goblin)
                    spawned_count += 1
        
        print(f"Spawned {spawned_count} enemies ({ogre_count} ogres, {spawned_count - ogre_count} goblins) on large map")
        print(f"Player position: ({player_x}, {player_y})")
        if self.enemies:
            print(f"First enemy at: ({self.enemies[0].x}, {self.enemies[0].y})")

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                # Changement d'arme
                self.player.handle_weapon_switch(event.key)

    def update(self, dt: float):
        self.current_time += dt
        self.player.update(dt, self.game_map, self.current_time, self.chest_manager)
        
        # Mettre à jour les coffres
        self.chest_manager.update(dt)
        
        # Mettre à jour les ennemis
        for enemy in self.enemies[:]:  # Copie pour éviter modifications pendant iteration
            if enemy.is_alive:
                enemy.update(dt, self.current_time)
            else:
                # Supprimer les ennemis morts après un délai (pour effet visuel)
                self.enemies.remove(enemy)
        
        # Vérifier les collisions d'attaque du joueur
        if self.player.is_attacking:
            xp_gained = self.player.deal_damage_to_enemies(self.enemies)
            if xp_gained > 0:
                self.player.gain_experience(xp_gained)

        screen_width = 800
        screen_height = 600
        self.camera_x = self.player.x - screen_width // 2
        self.camera_y = self.player.y - screen_height // 2

    def render(self, screen: pygame.Surface):
        # Render terrain layer first
        self.game_map.render_terrain(screen, self.camera_x, self.camera_y)

        # Render objects that should be behind the player (e.g., ground objects)
        # For now, let's render all objects behind the player
        self.game_map.render_objects(screen, self.camera_x, self.camera_y)
        
        # Render chests
        self.chest_manager.render_all(screen, self.camera_x, self.camera_y)

        # Render player on top of objects
        player_screen_x = self.player.x - self.camera_x
        player_screen_y = self.player.y - self.camera_y

        # Save current position and render player with camera offset
        old_x, old_y = self.player.x, self.player.y
        self.player.x = player_screen_x
        self.player.y = player_screen_y
        self.player.render(screen)
        self.player.x, self.player.y = old_x, old_y
        
        # Render enemies
        for enemy in self.enemies:
            if enemy.is_alive:
                enemy_screen_x = enemy.x - self.camera_x
                enemy_screen_y = enemy.y - self.camera_y
                
                # Save position and render with camera offset
                old_enemy_x, old_enemy_y = enemy.x, enemy.y
                enemy.x = enemy_screen_x
                enemy.y = enemy_screen_y
                enemy.render(screen)
                enemy.x, enemy.y = old_enemy_x, old_enemy_y

        # Render UI elements on top
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        health_text = font.render(
            f"Health: {self.player.health}/{self.player.max_health}",
            True,
            (255, 255, 255),
        )
        enemies_text = font.render(f"Enemies: {len(self.enemies)}", True, (255, 255, 255))
        
        # Chest info
        chest_stats = self.chest_manager.get_stats()
        chest_text = font.render(f"Chests: {chest_stats['opened_chests']}/{chest_stats['total_chests']}", True, (255, 255, 255))
        
        # Equipment info
        equipped_weapon = self.player.inventory.get_equipped_weapon()
        weapon_name = equipped_weapon.name if equipped_weapon else "None"
        damage = self.player.get_attack_damage()
        weapon_text = font.render(f"Weapon: {weapon_name} ({damage} dmg)", True, (255, 255, 255))
        
        # Interaction prompt
        player_center_x = self.player.x + self.player.width / 2
        player_center_y = self.player.y + self.player.height / 2
        nearby_chest = self.chest_manager.find_interactable_chest(player_center_x, player_center_y)
        
        # Controls info
        small_font = pygame.font.Font(None, 24)
        controls_text = small_font.render("1/2/3: Change Weapon | SPACE: Attack | WASD: Move | E: Interact", True, (200, 200, 200))

        screen.blit(level_text, (10, 10))
        screen.blit(health_text, (10, 50))
        screen.blit(enemies_text, (10, 90))
        screen.blit(chest_text, (10, 130))
        screen.blit(weapon_text, (10, 170))
        screen.blit(controls_text, (10, 210))
        
        # Interaction prompt
        if nearby_chest:
            interaction_font = pygame.font.Font(None, 32)
            prompt_text = interaction_font.render(nearby_chest.get_interaction_prompt(), True, (255, 255, 0))
            # Center the prompt at the bottom of the screen
            prompt_x = (screen.get_width() - prompt_text.get_width()) // 2
            prompt_y = screen.get_height() - 60
            screen.blit(prompt_text, (prompt_x, prompt_y))
