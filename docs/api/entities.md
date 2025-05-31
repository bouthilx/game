# Système d'Entités

Le système d'entités fournit la base pour tous les objets mobiles du jeu (joueur, ennemis, PNJ).

## Architecture de Base

### Entity (`game/entities/entity.py`)

Classe abstraite définissant les propriétés communes à tous les objets du jeu.

#### Propriétés Fondamentales
```python
class Entity:
    # Position et dimensions
    x: float              # Position X dans le monde
    y: float              # Position Y dans le monde
    width: int            # Largeur de collision
    height: int           # Hauteur de collision
    
    # Mouvement
    velocity_x: float     # Vitesse horizontale
    velocity_y: float     # Vitesse verticale
    speed: float          # Vitesse de base
    
    # État
    active: bool          # Entité active dans le jeu
```

#### Méthodes Core
- **`update(dt)`**: Mise à jour logique par frame
- **`render(screen, camera)`**: Affichage avec position caméra
- **`get_rect()`**: Rectangle de collision pour détection
- **`move(dt)`**: Application de la vélocité à la position

#### System de Collision
```python
def get_rect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height)

def check_collision(self, other):
    return self.get_rect().colliderect(other.get_rect())
```

---

### Player (`game/entities/player.py`)

Entité joueur avec contrôles, statistiques RPG et interaction avec le monde.

#### Spécialisations Player

##### Système de Contrôles
```python
# Input mapping
CONTROLS = {
    pygame.K_w: 'up',     pygame.K_UP: 'up',
    pygame.K_s: 'down',   pygame.K_DOWN: 'down', 
    pygame.K_a: 'left',   pygame.K_LEFT: 'left',
    pygame.K_d: 'right',  pygame.K_RIGHT: 'right'
}
```

##### Statistiques RPG
```python
class Player(Entity):
    # Stats de base
    health: int           # Points de vie actuels
    max_health: int       # Points de vie maximum
    level: int            # Niveau du joueur
    experience: int       # Expérience accumulée
    
    # Progression
    experience_to_next: int  # XP requis pour niveau suivant
    
    # Vitesses
    speed = 150          # Pixels par seconde
```

##### Système d'Expérience
```python
def gain_experience(self, amount):
    self.experience += amount
    while self.experience >= self.experience_to_next:
        self.level_up()

def level_up(self):
    self.level += 1
    self.max_health += 10        # +10 HP par niveau
    self.health = self.max_health # Guérison complète
    self.experience_to_next = int(self.experience_to_next * 1.5)
```

#### Système de Collision Avancé

##### Collision 4-Points
```python
def check_collision_at(self, x, y, bitmap_map):
    # Points de collision avec marge de 2 pixels
    margin = 2
    points = [
        (x + margin, y + margin),                    # Top-left
        (x + self.width - margin, y + margin),       # Top-right  
        (x + margin, y + self.height - margin),      # Bottom-left
        (x + self.width - margin, y + self.height - margin) # Bottom-right
    ]
    
    for px, py in points:
        if not bitmap_map.is_walkable_at(px, py):
            return True
    return False
```

##### Mouvement avec Collision
```python
def move(self, dt, bitmap_map):
    # Mouvement X séparé
    new_x = self.x + self.velocity_x * dt
    if not self.check_collision_at(new_x, self.y, bitmap_map):
        self.x = new_x
    
    # Mouvement Y séparé  
    new_y = self.y + self.velocity_y * dt
    if not self.check_collision_at(self.x, new_y, bitmap_map):
        self.y = new_y
```

#### Système de Combat

##### Gestion des Dégâts
```python
def take_damage(self, amount):
    self.health = max(0, self.health - amount)
    return self.health <= 0  # Retourne True si mort

def heal(self, amount):
    self.health = min(self.max_health, self.health + amount)
```

## Extensibilité du Système

### Ennemis (À Implémenter)
```python
class Enemy(Entity):
    # IA et comportement
    ai_state: str         # État de la machine d'état
    target: Entity        # Cible actuelle
    patrol_points: list   # Points de patrouille
    
    # Combat
    attack_damage: int    # Dégâts d'attaque
    detection_radius: int # Rayon de détection
    attack_range: int     # Portée d'attaque
```

### PNJ (À Implémenter)
```python
class NPC(Entity):
    # Dialogue
    dialogue: list        # Lignes de dialogue
    quests: list          # Quêtes disponibles
    
    # Commerce
    shop_items: list      # Objets à vendre
    buy_prices: dict      # Prix d'achat
```

## Patterns et Architecture

### Composition over Inheritance
- **Base Entity**: Fonctionnalités communes minimales
- **Components**: Extensions modulaires (stats, AI, inventory)
- **Mixins**: Comportements réutilisables

### Factory Pattern (Futur)
```python
class EntityFactory:
    @staticmethod
    def create_goblin(x, y):
        enemy = Enemy(x, y, 24, 24)
        enemy.health = 30
        enemy.speed = 100
        return enemy
```

### Observer Pattern (Futur)
```python
# Événements d'entité
player.on_level_up.subscribe(ui.update_level_display)
player.on_health_change.subscribe(ui.update_health_bar)
```

## Optimisation et Performance

### Culling Spatial
- **Rendu conditionnel**: Entités visibles seulement
- **Update partiel**: Entités proches du joueur prioritaires
- **Pooling**: Réutilisation d'objets ennemis

### Cache de Collision
- **Dirty flags**: Recalcul seulement si position modifiée
- **Spatial hashing**: Groupement par régions pour collision rapide\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: player\n\n### Player

**Hérite de**: Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float)

##### **handle_input**(self: )

##### **take_damage**(self: , damage: int)

##### **heal**(self: , amount: int)

##### **gain_experience**(self: , amount: int)

##### **level_up**(self: )

##### **can_move_to**(self: , x: float, y: float, game_map: ) → bool

##### **update**(self: , dt: float, game_map: )

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: entity\n\n### Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float, width: int, height: int)

##### **position**(self: ) → Tuple[float, float]

##### **position**(self: , pos: Tuple[float, float])

##### **rect**(self: ) → pygame.Rect

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: player\n\n### Player

**Hérite de**: Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float)

##### **handle_input**(self: )

##### **take_damage**(self: , damage: int)

##### **heal**(self: , amount: int)

##### **gain_experience**(self: , amount: int)

##### **level_up**(self: )

##### **can_move_to**(self: , x: float, y: float, game_map: ) → bool

##### **update**(self: , dt: float, game_map: )

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: entity\n\n### Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float, width: int, height: int)

##### **position**(self: ) → Tuple[float, float]

##### **position**(self: , pos: Tuple[float, float])

##### **rect**(self: ) → pygame.Rect

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: player\n\n### Player

**Hérite de**: Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float)

##### **handle_input**(self: , current_time: float)

##### **take_damage**(self: , damage: int)

##### **heal**(self: , amount: int)

##### **gain_experience**(self: , amount: int)

##### **level_up**(self: )

##### **can_attack**(self: , current_time: float) → bool

##### **start_attack**(self: , current_time: float)

##### **get_attack_rect**(self: ) → pygame.Rect

Get the rectangle representing the attack area.

##### **update_attack_state**(self: , current_time: float)

Update attack animation state.

##### **can_move_to**(self: , x: float, y: float, game_map: ) → bool

##### **update**(self: , dt: float, game_map: , current_time: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: entity\n\n### Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float, width: int, height: int)

##### **position**(self: ) → Tuple[float, float]

##### **position**(self: , pos: Tuple[float, float])

##### **rect**(self: ) → pygame.Rect

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: enemy\n\n### Enemy

**Hérite de**: Entity

Classe de base pour tous les ennemis.

#### Méthodes

##### **__init__**(self: , x: float, y: float, width: int, height: int)

##### **take_damage**(self: , damage: int) → bool

Prend des dégâts. Retourne True si l'ennemi meurt.

##### **can_attack**(self: , current_time: float) → bool

Vérifie si l'ennemi peut attaquer.

##### **distance_to_target**(self: ) → float

Calcule la distance au joueur cible.

##### **move_towards_target**(self: , dt: float)

Déplace l'ennemi vers sa cible.

##### **update_ai**(self: , dt: float, current_time: float)

Met à jour l'IA de l'ennemi.

##### **attack_target**(self: , current_time: float)

Attaque le joueur cible.

##### **check_collision_with_attack**(self: , attack_rect: pygame.Rect) → bool

Vérifie si l'ennemi est touché par une attaque.

##### **update**(self: , dt: float, current_time: float)

Met à jour l'ennemi.

##### **render**(self: , screen: pygame.Surface)

Affiche l'ennemi.

### Goblin

**Hérite de**: Enemy

Ennemi Gobelin - rapide avec peu de vie.

#### Méthodes

##### **__init__**(self: , x: float, y: float)

---\n\n### Module: player\n\n### Player

**Hérite de**: Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float)

##### **handle_input**(self: , current_time: float)

##### **take_damage**(self: , damage: int)

##### **heal**(self: , amount: int)

##### **gain_experience**(self: , amount: int)

##### **level_up**(self: )

##### **can_attack**(self: , current_time: float) → bool

##### **start_attack**(self: , current_time: float)

##### **get_attack_rect**(self: ) → pygame.Rect

Get the rectangle representing the attack area.

##### **update_attack_state**(self: , current_time: float)

Update attack animation state.

##### **check_attack_hits**(self: , enemies: list) → list

Vérifie si l'attaque touche des ennemis. Retourne la liste des ennemis touchés.

##### **deal_damage_to_enemies**(self: , enemies: list) → int

Inflige des dégâts aux ennemis touchés. Retourne l'XP gagnée.

##### **can_move_to**(self: , x: float, y: float, game_map: ) → bool

##### **update**(self: , dt: float, game_map: , current_time: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: entity\n\n### Entity

#### Méthodes

##### **__init__**(self: , x: float, y: float, width: int, height: int)

##### **position**(self: ) → Tuple[float, float]

##### **position**(self: , pos: Tuple[float, float])

##### **rect**(self: ) → pygame.Rect

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n