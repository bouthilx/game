# Moteur de Jeu

Le moteur de jeu fournit l'infrastructure de base pour la boucle de jeu, la gestion des scènes et l'affichage.

## Classes Principales

### Game (`game/engine/game.py`)

Classe principale qui orchestre toute l'application.

#### Responsabilités
- **Initialisation Pygame**: Configuration fenêtre et systèmes
- **Boucle de jeu principale**: Event handling → Update → Render
- **Gestion du temps**: Delta time pour animations frame-rate independent
- **Interface SceneManager**: Délégation de la logique aux scènes

#### Configuration
```python
# Paramètres d'affichage
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "Jeux Papa"
```

#### Cycle de Vie
1. **Initialisation**: Pygame, fenêtre, SceneManager
2. **Boucle principale**: Jusqu'à événement quit
3. **Nettoyage**: Fermeture propre de Pygame

---

### SceneManager (`game/engine/scene_manager.py`)

Gestionnaire de pile de scènes permettant navigation et états superposés.

#### Architecture Stack-Based
- **Push**: Ajoute scène au sommet (pause la précédente)
- **Pop**: Supprime scène courante (reprend la précédente)  
- **Replace**: Remplace scène courante par nouvelle

#### Gestion des États
```python
# Transitions entre scènes
def push_scene(scene):
    current_scene.pause()      # Pause scène actuelle
    stack.append(scene)        # Ajoute nouvelle scène
    new_scene.enter()          # Initialise nouvelle scène

def pop_scene():
    current_scene.exit()       # Nettoie scène courante
    stack.pop()               # Supprime de pile
    previous_scene.resume()    # Reprend scène précédente
```

#### Délégation des Événements
- **Update**: Seule la scène du sommet reçoit les updates
- **Render**: Toutes les scènes visibles sont rendues
- **Events**: Propagation aux scènes selon configuration

---

### Scene (`game/engine/scene.py`)

Classe abstraite de base pour tous les écrans et états de jeu.

#### Interface Standard
```python
class Scene:
    def enter(self):     # Initialisation à l'entrée
    def exit(self):      # Nettoyage à la sortie
    def pause(self):     # Pause (autre scène par-dessus)
    def resume(self):    # Reprise après pause
    
    def update(self, dt): # Mise à jour logique
    def render(self, screen): # Affichage
    def handle_event(self, event): # Gestion événements
```

#### Implémentations Concrètes
- **GameScene**: Scène de jeu principale avec world et player
- **MenuScene**: (À implémenter) Menus et interfaces
- **PauseScene**: (À implémenter) Écran de pause

## Flux d'Exécution

### Boucle Principale
```python
while running:
    # 1. Gestion des événements
    for event in pygame.event.get():
        scene_manager.handle_event(event)
    
    # 2. Mise à jour logique
    dt = clock.tick(FPS) / 1000.0
    scene_manager.update(dt)
    
    # 3. Rendu
    screen.fill(BLACK)
    scene_manager.render(screen)
    pygame.display.flip()
```

### Delta Time
- **Indépendance frame-rate**: Mouvement basé sur temps réel
- **Calcul**: Millisecondes entre frames converties en secondes
- **Usage**: Multiplication des vitesses par `dt` pour cohérence

## Extensibilité

### Nouvelles Scènes
1. **Hériter** de la classe Scene
2. **Implémenter** les méthodes de lifecycle
3. **Ajouter** logique spécifique dans update/render
4. **Transition** via SceneManager

### Systèmes Globaux
- **Audio**: Intégrable via Game class
- **Input Manager**: Extension possible pour contrôles complexes
- **Resource Manager**: Chargement centralisé des assets

## Patterns Utilisés

### State Pattern
- **SceneManager**: Context gérant différents états
- **Scene**: States avec comportements spécifiques
- **Transitions**: Changements d'état contrôlés

### Template Method
- **Scene**: Définit squelette des méthodes
- **Implémentations**: Spécialisent comportements
- **Lifecycle**: Séquence standardisée\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: scene_manager\n\n### SceneManager

#### Méthodes

##### **__init__**(self: )

##### **push_scene**(self: , scene: Scene)

##### **pop_scene**(self: )

##### **replace_scene**(self: , scene: Scene)

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: game\n\n### Game

#### Méthodes

##### **__init__**(self: , width: int, height: int)

##### **handle_events**(self: )

##### **update**(self: , dt: float)

##### **render**(self: )

##### **run**(self: )

---\n\n### Module: scene\n\n### Scene

**Hérite de**: ABC

#### Méthodes

##### **__init__**(self: )

##### **on_enter**(self: )

##### **on_exit**(self: )

##### **on_pause**(self: )

##### **on_resume**(self: )

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: scene_manager\n\n### SceneManager

#### Méthodes

##### **__init__**(self: )

##### **push_scene**(self: , scene: Scene)

##### **pop_scene**(self: )

##### **replace_scene**(self: , scene: Scene)

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: game\n\n### Game

#### Méthodes

##### **__init__**(self: , width: int, height: int)

##### **handle_events**(self: )

##### **update**(self: , dt: float)

##### **render**(self: )

##### **run**(self: )

---\n\n### Module: scene\n\n### Scene

**Hérite de**: ABC

#### Méthodes

##### **__init__**(self: )

##### **on_enter**(self: )

##### **on_exit**(self: )

##### **on_pause**(self: )

##### **on_resume**(self: )

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: scene_manager\n\n### SceneManager

#### Méthodes

##### **__init__**(self: )

##### **push_scene**(self: , scene: Scene)

##### **pop_scene**(self: )

##### **replace_scene**(self: , scene: Scene)

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: game\n\n### Game

#### Méthodes

##### **__init__**(self: , width: int, height: int)

##### **handle_events**(self: )

##### **update**(self: , dt: float)

##### **render**(self: )

##### **run**(self: )

---\n\n### Module: scene\n\n### Scene

**Hérite de**: ABC

#### Méthodes

##### **__init__**(self: )

##### **on_enter**(self: )

##### **on_exit**(self: )

##### **on_pause**(self: )

##### **on_resume**(self: )

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\n\n### Module: scene_manager\n\n### SceneManager

#### Méthodes

##### **__init__**(self: )

##### **push_scene**(self: , scene: Scene)

##### **pop_scene**(self: )

##### **replace_scene**(self: , scene: Scene)

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n### Module: game\n\n### Game

#### Méthodes

##### **__init__**(self: , width: int, height: int)

##### **handle_events**(self: )

##### **update**(self: , dt: float)

##### **render**(self: )

##### **run**(self: )

---\n\n### Module: scene\n\n### Scene

**Hérite de**: ABC

#### Méthodes

##### **__init__**(self: )

##### **on_enter**(self: )

##### **on_exit**(self: )

##### **on_pause**(self: )

##### **on_resume**(self: )

##### **handle_event**(self: , event: pygame.event.Event)

##### **update**(self: , dt: float)

##### **render**(self: , screen: pygame.Surface)

---\n\n