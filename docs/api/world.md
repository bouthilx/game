# Système de Monde

Le système de monde gère les cartes, terrains, objets et environnements du jeu via un système bitmap innovant.

## Architecture du Monde

### BitmapMap (`game/world/bitmap_map.py`)

Système de cartes basé sur des images PNG où les couleurs de pixels définissent les types de terrain et objets.

#### Concept Core
```python
class BitmapMap:
    # Données de la carte
    terrain_data: list[list]   # Matrice des types de terrain
    object_data: list[list]    # Matrice des objets placés
    
    # Dimensions
    width: int                 # Largeur en tuiles
    height: int               # Hauteur en tuiles
    tile_size: int = 32       # Taille tuile en pixels
```

#### Chargement depuis PNG
```python
def load_from_image(self, terrain_path, object_path=None):
    # Chargement image terrain
    terrain_image = pygame.image.load(terrain_path)
    
    # Conversion pixels → types de terrain
    for y in range(height):
        for x in range(width):
            pixel_color = terrain_image.get_at((x, y))
            terrain_type = TileTypes.get_type_from_color(pixel_color)
            self.terrain_data[y][x] = terrain_type
```

#### Système de Collision
```python
def is_walkable_at(self, world_x, world_y):
    # Conversion coordonnées monde → tuile
    tile_x = int(world_x // self.tile_size)
    tile_y = int(world_y // self.tile_size)
    
    # Vérification terrain
    terrain = self.get_terrain_at(tile_x, tile_y)
    if not terrain.walkable:
        return False
    
    # Vérification objet
    obj = self.get_object_at(tile_x, tile_y)
    if obj and not obj.walkable:
        return False
    
    return True
```

---

### TileTypes (`game/world/tile_types.py`)

Définition des types de terrain avec propriétés et apparence.

#### Types de Terrain Standard
```python
class TileType:
    GRASS = TileType("grass", (34, 139, 34), walkable=True)
    DIRT = TileType("dirt", (139, 69, 19), walkable=True)
    STONE = TileType("stone", (128, 128, 128), walkable=True)
    WATER = TileType("water", (0, 0, 255), walkable=False)
    WALL = TileType("wall", (165, 42, 42), walkable=False)
    SPAWN = TileType("spawn", (255, 0, 0), walkable=True)
    VOID = TileType("void", (0, 0, 0), walkable=False)
```

#### Système de Couleurs
```python
@staticmethod
def get_type_from_color(color):
    color_map = {
        (34, 139, 34): TileType.GRASS,
        (139, 69, 19): TileType.DIRT,
        (128, 128, 128): TileType.STONE,
        # ... autres mappings
    }
    return color_map.get(color, TileType.VOID)
```

---

### GameObject (`game/world/game_object.py`)

Objets interactifs et décoratifs placés dans le monde.

#### Propriétés d'Objet
```python
class GameObject:
    name: str             # Identifiant de l'objet
    color: tuple         # Couleur de placement sur carte
    size: tuple          # Dimensions en tuiles (w, h)
    walkable: bool       # Traversable par entités
    sprite_path: str     # Chemin vers sprite
```

#### Types d'Objets Standard
```python
# Végétation
SMALL_TREE = GameObject("small_tree", (0, 255, 0), (1, 1), False)
LARGE_TREE = GameObject("large_tree", (0, 200, 0), (2, 2), False)
BUSH = GameObject("bush", (0, 150, 0), (1, 1), False)

# Structures
HOUSE = GameObject("house", (255, 255, 0), (3, 2), False)
SHED = GameObject("shed", (200, 200, 0), (2, 1), False)
WELL = GameObject("well", (150, 150, 150), (1, 1), False)

# Interactifs
CHEST = GameObject("chest", (255, 165, 0), (1, 1), True)
BARREL = GameObject("barrel", (139, 69, 19), (1, 1), False)
```

## Rendu et Caméra

### Système de Caméra
```python
class Camera:
    x: float             # Position X de la caméra
    y: float             # Position Y de la caméra
    
    def follow_player(self, player, dt):
        # Caméra centrée sur joueur avec offset
        target_x = player.x - WINDOW_WIDTH // 2
        target_y = player.y - WINDOW_HEIGHT // 2
        
        # Mouvement fluide vers cible
        self.x += (target_x - self.x) * follow_speed * dt
        self.y += (target_y - self.y) * follow_speed * dt
```

### Viewport Culling
```python
def render(self, screen, camera):
    # Calcul zone visible
    start_x = max(0, int(camera.x // self.tile_size))
    start_y = max(0, int(camera.y // self.tile_size))
    end_x = min(self.width, start_x + visible_tiles_x + 1)
    end_y = min(self.height, start_y + visible_tiles_y + 1)
    
    # Rendu seulement des tuiles visibles
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            self.render_tile(screen, x, y, camera)
```

## Système de Spawn

### Placement Intelligent
```python
def find_safe_spawn_position(self):
    # Recherche positions spawn valides
    spawn_points = []
    for y in range(self.height):
        for x in range(self.width):
            if self.terrain_data[y][x] == TileType.SPAWN:
                if self.is_area_clear(x, y, 2, 2):  # Zone 2x2 libre
                    spawn_points.append((x * 32, y * 32))
    
    return random.choice(spawn_points) if spawn_points else (100, 100)
```

## Data-Driven Design

### Avantages du Système Bitmap
- **Édition visuelle**: Cartes créées avec éditeurs d'image
- **Rapidité**: Conception de niveaux sans outils spécialisés
- **Flexibilité**: Modification facile des layouts
- **Précision**: Contrôle pixel-perfect du placement

### Workflow de Création
1. **Image terrain**: PNG avec couleurs définissant types terrain
2. **Image objets**: PNG séparée pour placement d'objets
3. **Chargement**: Parsing automatique vers structures de données
4. **Test**: Jeu immédiatement avec nouvelle carte

## Extensions Futures

### Multi-Maps
```python
class WorldManager:
    current_map: BitmapMap
    maps: dict[str, BitmapMap]
    
    def transition_to(self, map_name, spawn_point):
        self.current_map = self.maps[map_name]
        player.x, player.y = spawn_point
```

### Objets Interactifs
```python
class InteractiveObject(GameObject):
    on_interact: callable    # Fonction appelée lors interaction
    state: dict             # État persistant de l'objet
    
    def interact(self, player):
        if self.on_interact:
            self.on_interact(player, self)
```

### Effets Environnementaux
```python
class EnvironmentalZone:
    area: pygame.Rect       # Zone d'effet
    effect_type: str        # Type d'effet (froid, poison, etc.)
    intensity: float        # Intensité de l'effet
    
    def apply_to_entity(self, entity):
        if self.area.colliderect(entity.get_rect()):
            entity.apply_status_effect(self.effect_type, self.intensity)
```\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: bitmap_map\n\n### BitmapMap

#### Méthodes

##### **__init__**(self: , map_path: str, tile_size: int)

##### **find_safe_spawn_position**(self: ) → Tuple[float, float]

Find a safe spawn position after objects are loaded.

##### **is_player_spawn_safe**(self: , x: float, y: float, player_width: int, player_height: int) → bool

Check if a player-sized rectangle can be safely placed at this position.

##### **get_tile_at_pixel**(self: , world_x: float, world_y: float) → TileType

##### **get_tile_at_grid**(self: , tile_x: int, tile_y: int) → TileType

##### **is_walkable**(self: , world_x: float, world_y: float) → bool

##### **get_objects_at_point**(self: , world_x: float, world_y: float) → List[GameObject]

Get all objects that contain the given point.

##### **get_objects_in_area**(self: , x: float, y: float, width: float, height: float) → List[GameObject]

Get all objects that intersect with the given area.

##### **get_world_size**(self: ) → Tuple[int, int]

##### **render_terrain**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the terrain layer.

##### **render_objects**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the objects layer.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render terrain and objects (for backward compatibility).

---\n\n### Module: object_types\n\n### ObjectType

#### Méthodes

##### **__init__**(self: , name: str, size: Tuple[int, int], sprite_path: str, walkable: bool)

---\n\n### Module: tile_types\n\n### TileType

#### Méthodes

##### **__init__**(self: , name: str, walkable: bool, color: Tuple[int, int, int])

---\n\n### Module: game_object\n\n### GameObject

#### Méthodes

##### **__init__**(self: , name: str, x: float, y: float, width: int, height: int, sprite_path: str, walkable: bool)

##### **rect**(self: ) → pygame.Rect

##### **get_tile_coverage**(self: , tile_size: int) → list[Tuple[int, int]]

Get list of tile coordinates this object covers.

##### **is_point_inside**(self: , x: float, y: float) → bool

Check if a point is inside this object.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render the object sprite.

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: bitmap_map\n\n### BitmapMap

#### Méthodes

##### **__init__**(self: , map_path: str, tile_size: int)

##### **find_safe_spawn_position**(self: ) → Tuple[float, float]

Find a safe spawn position after objects are loaded.

##### **is_player_spawn_safe**(self: , x: float, y: float, player_width: int, player_height: int) → bool

Check if a player-sized rectangle can be safely placed at this position.

##### **get_tile_at_pixel**(self: , world_x: float, world_y: float) → TileType

##### **get_tile_at_grid**(self: , tile_x: int, tile_y: int) → TileType

##### **is_walkable**(self: , world_x: float, world_y: float) → bool

##### **get_objects_at_point**(self: , world_x: float, world_y: float) → List[GameObject]

Get all objects that contain the given point.

##### **get_objects_in_area**(self: , x: float, y: float, width: float, height: float) → List[GameObject]

Get all objects that intersect with the given area.

##### **get_world_size**(self: ) → Tuple[int, int]

##### **render_terrain**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the terrain layer.

##### **render_objects**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the objects layer.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render terrain and objects (for backward compatibility).

---\n\n### Module: object_types\n\n### ObjectType

#### Méthodes

##### **__init__**(self: , name: str, size: Tuple[int, int], sprite_path: str, walkable: bool)

---\n\n### Module: tile_types\n\n### TileType

#### Méthodes

##### **__init__**(self: , name: str, walkable: bool, color: Tuple[int, int, int])

---\n\n### Module: game_object\n\n### GameObject

#### Méthodes

##### **__init__**(self: , name: str, x: float, y: float, width: int, height: int, sprite_path: str, walkable: bool)

##### **rect**(self: ) → pygame.Rect

##### **get_tile_coverage**(self: , tile_size: int) → list[Tuple[int, int]]

Get list of tile coordinates this object covers.

##### **is_point_inside**(self: , x: float, y: float) → bool

Check if a point is inside this object.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render the object sprite.

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: bitmap_map\n\n### BitmapMap

#### Méthodes

##### **__init__**(self: , map_path: str, tile_size: int)

##### **find_safe_spawn_position**(self: ) → Tuple[float, float]

Find a safe spawn position after objects are loaded.

##### **is_player_spawn_safe**(self: , x: float, y: float, player_width: int, player_height: int) → bool

Check if a player-sized rectangle can be safely placed at this position.

##### **get_tile_at_pixel**(self: , world_x: float, world_y: float) → TileType

##### **get_tile_at_grid**(self: , tile_x: int, tile_y: int) → TileType

##### **is_walkable**(self: , world_x: float, world_y: float) → bool

##### **get_objects_at_point**(self: , world_x: float, world_y: float) → List[GameObject]

Get all objects that contain the given point.

##### **get_objects_in_area**(self: , x: float, y: float, width: float, height: float) → List[GameObject]

Get all objects that intersect with the given area.

##### **get_world_size**(self: ) → Tuple[int, int]

##### **render_terrain**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the terrain layer.

##### **render_objects**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the objects layer.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render terrain and objects (for backward compatibility).

---\n\n### Module: object_types\n\n### ObjectType

#### Méthodes

##### **__init__**(self: , name: str, size: Tuple[int, int], sprite_path: str, walkable: bool)

---\n\n### Module: tile_types\n\n### TileType

#### Méthodes

##### **__init__**(self: , name: str, walkable: bool, color: Tuple[int, int, int])

---\n\n### Module: game_object\n\n### GameObject

#### Méthodes

##### **__init__**(self: , name: str, x: float, y: float, width: int, height: int, sprite_path: str, walkable: bool)

##### **rect**(self: ) → pygame.Rect

##### **get_tile_coverage**(self: , tile_size: int) → list[Tuple[int, int]]

Get list of tile coordinates this object covers.

##### **is_point_inside**(self: , x: float, y: float) → bool

Check if a point is inside this object.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render the object sprite.

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: bitmap_map\n\n### BitmapMap

#### Méthodes

##### **__init__**(self: , map_path: str, tile_size: int)

##### **find_safe_spawn_position**(self: ) → Tuple[float, float]

Find a safe spawn position after objects are loaded.

##### **is_player_spawn_safe**(self: , x: float, y: float, player_width: int, player_height: int) → bool

Check if a player-sized rectangle can be safely placed at this position.

##### **get_tile_at_pixel**(self: , world_x: float, world_y: float) → TileType

##### **get_tile_at_grid**(self: , tile_x: int, tile_y: int) → TileType

##### **is_walkable**(self: , world_x: float, world_y: float) → bool

##### **get_objects_at_point**(self: , world_x: float, world_y: float) → List[GameObject]

Get all objects that contain the given point.

##### **get_objects_in_area**(self: , x: float, y: float, width: float, height: float) → List[GameObject]

Get all objects that intersect with the given area.

##### **get_world_size**(self: ) → Tuple[int, int]

##### **render_terrain**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the terrain layer.

##### **render_objects**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the objects layer.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render terrain and objects (for backward compatibility).

---\n\n### Module: object_types\n\n### ObjectType

#### Méthodes

##### **__init__**(self: , name: str, size: Tuple[int, int], sprite_path: str, walkable: bool)

---\n\n### Module: tile_types\n\n### TileType

#### Méthodes

##### **__init__**(self: , name: str, walkable: bool, color: Tuple[int, int, int])

---\n\n### Module: game_object\n\n### GameObject

#### Méthodes

##### **__init__**(self: , name: str, x: float, y: float, width: int, height: int, sprite_path: str, walkable: bool)

##### **rect**(self: ) → pygame.Rect

##### **get_tile_coverage**(self: , tile_size: int) → list[Tuple[int, int]]

Get list of tile coordinates this object covers.

##### **is_point_inside**(self: , x: float, y: float) → bool

Check if a point is inside this object.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render the object sprite.

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: bitmap_map\n\n### BitmapMap

#### Méthodes

##### **__init__**(self: , map_path: str, tile_size: int)

##### **find_safe_spawn_position**(self: ) → Tuple[float, float]

Find a safe spawn position after objects are loaded.

##### **is_player_spawn_safe**(self: , x: float, y: float, player_width: int, player_height: int) → bool

Check if a player-sized rectangle can be safely placed at this position.

##### **get_tile_at_pixel**(self: , world_x: float, world_y: float) → TileType

##### **get_tile_at_grid**(self: , tile_x: int, tile_y: int) → TileType

##### **is_walkable**(self: , world_x: float, world_y: float) → bool

##### **get_objects_at_point**(self: , world_x: float, world_y: float) → List[GameObject]

Get all objects that contain the given point.

##### **get_objects_in_area**(self: , x: float, y: float, width: float, height: float) → List[GameObject]

Get all objects that intersect with the given area.

##### **get_world_size**(self: ) → Tuple[int, int]

##### **render_terrain**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the terrain layer.

##### **render_objects**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render only the objects layer.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render terrain and objects (for backward compatibility).

---\n\n### Module: object_types\n\n### ObjectType

#### Méthodes

##### **__init__**(self: , name: str, size: Tuple[int, int], sprite_path: str, walkable: bool)

---\n\n### Module: tile_types\n\n### TileType

#### Méthodes

##### **__init__**(self: , name: str, walkable: bool, color: Tuple[int, int, int])

---\n\n### Module: game_object\n\n### GameObject

#### Méthodes

##### **__init__**(self: , name: str, x: float, y: float, width: int, height: int, sprite_path: str, walkable: bool)

##### **rect**(self: ) → pygame.Rect

##### **get_tile_coverage**(self: , tile_size: int) → list[Tuple[int, int]]

Get list of tile coordinates this object covers.

##### **is_point_inside**(self: , x: float, y: float) → bool

Check if a point is inside this object.

##### **render**(self: , screen: pygame.Surface, camera_x: float, camera_y: float)

Render the object sprite.

---\n\n