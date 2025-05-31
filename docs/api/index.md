# Architecture API

Cette section documente l'architecture technique du code de Jeux Papa, organisée autour d'un moteur de jeu modulaire basé sur Pygame.

## Vue d'ensemble de l'Architecture

### Moteur de Jeu Custom
- **Framework**: Pygame 2.5.0+
- **Architecture**: Scene-based avec gestion d'états
- **Rendu**: Immediate mode rendering à 60 FPS
- **Résolution**: Fenêtre 800x600 pixels

### Organisation du Code

```
game/
├── engine/          # Cœur du moteur de jeu
├── entities/        # Système d'entités (joueur, ennemis)
├── scenes/          # Gestion des écrans de jeu
├── world/          # Système de monde et cartes
└── systems/        # Systèmes de jeu (son, input, etc.)
```

## Composants Principaux

### [Moteur de Jeu](engine.md)
- **Game**: Boucle principale et gestion globale
- **SceneManager**: Pile de scènes avec transitions
- **Scene**: Classes de base pour les différents écrans

### [Système d'Entités](entities.md)
- **Entity**: Classe de base pour tous les objets du jeu
- **Player**: Entité joueur avec contrôles et statistiques RPG
- Architecture extensible pour ennemis et PNJ

### [Système de Monde](world.md)
- **BitmapMap**: Système de cartes basé sur images PNG
- **TileTypes**: Définition des terrains et propriétés
- **GameObject**: Objets interactifs dans le monde

## Patterns d'Architecture

### Scene Management
- **Stack-based**: Empilement de scènes pour menus/pauses
- **Lifecycle**: Méthodes enter/exit/pause/resume
- **State Management**: Isolation des états de jeu

### Entity-Component Pattern
- **Base Entity**: Position, vélocité, collision
- **Spécialisations**: Player avec stats RPG étendues
- **Extensibilité**: Prêt pour ennemis et systèmes complexes

### Data-Driven Design
- **Bitmap Maps**: Terrain défini par couleurs PNG
- **Configuration**: Types de tuiles et objets externalisés
- **Assets**: Système modulaire pour sprites et sons

## Qualité et Tests

### Couverture de Tests
- **97%+ de couverture**: Tests unitaires et fonctionnels
- **Pytest**: Framework de test principal
- **CI/CD**: Intégration continue avec Tox

### Standards de Code
- **Ruff**: Linting et formatage automatique
- **Type Hints**: Support Python 3.8+
- **Documentation**: Docstrings pour toutes les classes publiques

## Points d'Extension

### Systèmes Prêts
- **Entity System**: Extensible pour ennemis et PNJ
- **Scene System**: Prêt pour menus et multiple zones
- **Asset Pipeline**: Support sprites et animations
- **Map System**: Multi-cartes et objets interactifs

### Prochaines Implémentations
- **Combat System**: Extension du système d'entités
- **Inventory System**: Gestion d'objets et équipement
- **Enemy AI**: Machines d'états pour comportements
- **Sound System**: Audio et effets sonores